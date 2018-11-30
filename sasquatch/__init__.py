import logging


__version__ = '0.0.0'

from . import cli
from .util.conf import config
from .util.log import setupLogging

setupLogging(config.meta.name, __version__, loglvl=config.logging.loglvl)

from . import entry
