from pkg_resources import DistributionNotFound, get_distribution

from mkdocs_callouts_to_admonitions.plugin import CalloutsToAdmonitionsPlugin

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass
