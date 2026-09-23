""" This tool allows generation of gettext .mo compiled files, pot files from source code files
and pot files for merging.

Three new builders are added into the constructed environment:

- gettextMoFile: generates .mo file from .pot file using msgfmt.
- gettextPotFile: Generates .pot file from source code files.
- gettextMergePotFile: Creates a .pot file appropriate for merging into existing .po files.

To properly configure get text, define the following variables:

- gettext_package_bugs_address
- gettext_package_name
- gettext_package_version


"""
import array
import ast
import os
import shutil
import struct
from SCons.Action import Action


def po2mo(po_path, mo_path):
	MESSAGES = {}
	with open(po_path, 'r', encoding='utf-8', errors='replace') as f:
		lines = f.readlines()
	section = None
	msgid, msgstr, msgctxt = [], [], []

	def add(msgid, msgstr, msgctxt):
		id_str = ''.join(msgid)
		val_str = ''.join(msgstr)
		if msgctxt:
			id_str = ''.join(msgctxt) + '\x04' + id_str
		MESSAGES[id_str] = val_str

	for line in lines:
		line = line.strip()
		if not line or line.startswith('#'):
			continue
		if line.startswith('msgctxt '):
			if section == 'STR':
				add(msgid, msgstr, msgctxt)
				msgid, msgstr, msgctxt = [], [], []
			section = 'msgctxt'
			msgctxt.append(ast.literal_eval(line[8:].strip()))
		elif line.startswith('msgid '):
			if section == 'STR':
				add(msgid, msgstr, msgctxt)
				msgid, msgstr, msgctxt = [], [], []
			section = 'ID'
			msgid.append(ast.literal_eval(line[6:].strip()))
		elif line.startswith('msgstr '):
			section = 'STR'
			msgstr.append(ast.literal_eval(line[7:].strip()))
		elif line.startswith('"') and line.endswith('"'):
			if section == 'ID':
				msgid.append(ast.literal_eval(line))
			elif section == 'STR':
				msgstr.append(ast.literal_eval(line))
			elif section == 'msgctxt':
				msgctxt.append(ast.literal_eval(line))

	if section == 'STR':
		add(msgid, msgstr, msgctxt)

	keys = sorted(MESSAGES.keys())
	offsets = []
	ids = b''
	strs = b''
	for key in keys:
		key_bytes = key.encode('utf-8') + b'\x00'
		val_bytes = MESSAGES[key].encode('utf-8') + b'\x00'
		offsets.append((len(ids), len(key_bytes) - 1, len(strs), len(val_bytes) - 1))
		ids += key_bytes
		strs += val_bytes

	keystart = 7 * 4 + 16 * len(keys)
	valstart = keystart + len(ids)
	koffsets = []
	voffsets = []
	for o1, l1, o2, l2 in offsets:
		koffsets += [l1, o1 + keystart]
		voffsets += [l2, o2 + valstart]

	output = struct.pack('Iiiiiii', 0x950412DE, 0, len(keys), 7 * 4, 7 * 4 + len(keys) * 8, 0, 0)
	output += array.array('i', koffsets).tobytes()
	output += array.array('i', voffsets).tobytes()
	output += ids + strs

	os.makedirs(os.path.dirname(os.path.abspath(mo_path)), exist_ok=True)
	with open(mo_path, 'wb') as f:
		f.write(output)
	return 0


def exists(env):
	return True


XGETTEXT_COMMON_ARGS = (
	"--msgid-bugs-address='$gettext_package_bugs_address' "
	"--package-name='$gettext_package_name' "
	"--package-version='$gettext_package_version' "
	"--keyword=pgettext:1c,2 "
	"-c -o $TARGET $SOURCES"
)


def generate(env):
	env.SetDefault(gettext_package_bugs_address="example@example.com")
	env.SetDefault(gettext_package_name="")
	env.SetDefault(gettext_package_version="")

	if shutil.which("msgfmt"):
		mo_action = Action("msgfmt -o $TARGET $SOURCE", "Compiling translation $SOURCE")
	else:
		mo_action = Action(
			lambda target, source, env: po2mo(source[0].abspath, target[0].abspath) and None,
			"Compiling translation $SOURCE"
		)

	env['BUILDERS']['gettextMoFile'] = env.Builder(
		action=mo_action,
		suffix=".mo",
		src_suffix=".po"
	)

	env['BUILDERS']['gettextPotFile'] = env.Builder(
		action=Action("xgettext " + XGETTEXT_COMMON_ARGS, "Generating pot file $TARGET"),
		suffix=".pot")

	env['BUILDERS']['gettextMergePotFile'] = env.Builder(
		action=Action(
			"xgettext " + "--omit-header --no-location " + XGETTEXT_COMMON_ARGS,
			"Generating pot file $TARGET"
		),
		suffix=".pot"
	)
