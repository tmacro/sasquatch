import logging
import sys

from .util.arg import flag, option


@flag('--version', dest='runtime.version_flag')
def version(*args, **kwargs):
	return True

@flag('-v', '--verbose', dest='logging.loglvl')
def verbose(*args, **kwargs):
	return 'debug'


@option('-a', '--access-key', dest='runtime.credentials.aws_access_key_id', metavar='ACCESS_KEY')
def access_key(value):
	return value

@option('-s', '--secret-key', dest='runtime.credentials.aws_secret_access_key', metavar='SECRET_KEY')
def secret_key(value):
	return value

@option('-p', '--profile', dest='runtime.credentials.profile', metavar='PROFILE')
def profile(value):
	return value

@option('-f', '--file', dest='runtime.file', metavar='FILENAME')
def script_file(value):
	return value

@option(dest='runtime.script', nargs='?', metavar='SCRIPT')
def script_cmd(value):
	return value
