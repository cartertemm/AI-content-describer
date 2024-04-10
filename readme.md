# AI Content Describer for NVDA third-party dependencies

this branch exists along-side *main* for the simple purpose of providing a single release which will maintain all of the zipped third-party dependency releases broken down by Python version.

It will be updated rarely, under the following circumstances:

* When a new version of the addon is released that introduces new modules.
* When a major security advisory is found affecting one of the dependencies.
* When NVDA increments its python version or maybe architecture (one day).

Since Github does not allow us to exclude source directories in a release, we rely on .gitattributes and .gitignore with most of the root files/folders, and export-ignore directives in the former case to remove redundant code.
