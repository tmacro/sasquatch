import logging


__version__ = '0.0.1'

from . import cli
from .util.conf import config
from .util.log import setupLogging

setupLogging(config.meta.name, __version__, **config.logging._asdict())

from . import entry
