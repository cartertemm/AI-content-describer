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
from SCons.Action import Action


def exists(env):
	return True


XGETTEXT_COMMON_ARGS = (
	"--msgid-bugs-address='$gettext_package_bugs_address' "
	"--package-name='$gettext_package_name' "
	"--package-version='$gettext_package_version' "
	"--keyword=pgettext:1c,2 "
	"-c -o $TARGET $SOURCES"
)


def _set_pot_charset(target, source, env):
	"""xgettext writes charset=CHARSET when every string is ASCII. Translation tools expect UTF-8."""
	path = str(target[0])
	with open(path, encoding="utf-8", newline="") as f:
		text = f.read()
	with open(path, "w", encoding="utf-8", newline="") as f:
		f.write(text.replace("charset=CHARSET", "charset=UTF-8", 1))


def generate(env):
	env.SetDefault(gettext_package_bugs_address="example@example.com")
	env.SetDefault(gettext_package_name="")
	env.SetDefault(gettext_package_version="")

	env['BUILDERS']['gettextMoFile'] = env.Builder(
		action=Action("msgfmt -o $TARGET $SOURCE", "Compiling translation $SOURCE"),
		suffix=".mo",
		src_suffix=".po"
	)

	env['BUILDERS']['gettextPotFile'] = env.Builder(
		action=[
			Action("xgettext " + XGETTEXT_COMMON_ARGS, "Generating pot file $TARGET"),
			Action(_set_pot_charset, None),
		],
		suffix=".pot")

	env['BUILDERS']['gettextMergePotFile'] = env.Builder(
		action=Action(
			"xgettext " + "--omit-header --no-location " + XGETTEXT_COMMON_ARGS,
			"Generating pot file $TARGET"
		),
		suffix=".pot"
	)
