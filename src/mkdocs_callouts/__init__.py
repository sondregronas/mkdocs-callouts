from importlib.metadata import version, PackageNotFoundError

from mkdocs_callouts.plugin import CalloutsPlugin

try:
    __version__ = version("mkdocs-callouts")
except PackageNotFoundError:  # pragma: no cover
    # package is not installed
    pass
