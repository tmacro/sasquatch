from .base import SQError, BaseErrorHelper
from .context import ContextAwareError

class ExecutionError(SQError):
	'''raised when an error is encountered during script execution'''

class ExecErrorHelper(BaseErrorHelper):
	_default = ExecutionError
	@staticmethod
	def throw(cls = ExecutionError, **kwargs):
		if 'ctx' in kwargs and kwargs['ctx'] is not None:
			ctx = kwargs.get('ctx')
			return BaseErrorHelper.throw(cls, **ctx._asdict(), **kwargs)


class MissingKeywordError(ExecutionError):
	'''Raised when a required keyword argument can not be collected'''
	_msg = 'Unable to collect keyword {keyword}'

class InvalidFilePathError(ContextAwareError, ExecutionError):
	'''Raised when a file path passed as input does not exist or is invalid'''
	_msg = 'Path {filepath} is not a valid location'
