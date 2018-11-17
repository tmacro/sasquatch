from .util.log import setupLogging
import logging

__version__ = '0.0.0'

setupLogging('sasquatch', __version__, loglvl=logging.INFO)

from . import entry
