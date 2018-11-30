from .base import SQError, BaseErrorHelper

class ExecutionError(SQError):
	'''raised when an error is encountered during script execution'''

class ExecErrorHelper(BaseErrorHelper):
	_default = ExecutionError

class MissingKeywordError(ExecutionError):
	'''Raised when a required keyword argument can not be collected'''
	_msg = 'Unable to collect keyword {keyword}'
