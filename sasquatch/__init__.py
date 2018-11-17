import logging

from .util.log import setupLogging

__version__ = '0.0.0'

setupLogging('sasquatch', __version__, loglvl=logging.INFO)

from . import entry
