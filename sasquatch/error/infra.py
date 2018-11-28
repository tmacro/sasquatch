from .base import SQError, BaseErrorHelper


class InterpreterError(SQError):
	'''Base error for underlying Sasquatch components not related to user code'''


class InfraErrorHelper(BaseErrorHelper):
	_default = InterpreterError


class InvalidVerbDefinitionError(InterpreterError):
	'''Raised when a invalid Verb definition is found during init'''
	_msg = 'Verb {verb}: missing required attribute {attr}'

class InvalidVerbAction(InterpreterError):
	'''Raised when a unknown action is found during init'''
	_msg = 'Verb {verb}: {action} is not a valid S3 operation!'
