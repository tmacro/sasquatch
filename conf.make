DOCKER_USER = tmacro
DOCKER_REPO = sasquatch
PYPI_PKG    = sasquatch

PKG_NAME = sasquatch
PKG_VERSION = $(shell awk '/^__version__/{print $$3}' sasquatch/__init__.py | tr -d "'")
