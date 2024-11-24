from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mktimeline")
except PackageNotFoundError:
    __version__ = "unknown"
