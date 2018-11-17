from .base import SQError, BaseErrorHelper


class InterpreterError(SQError):
	'''Base error for underlying Sasquatch components not related to user code'''


class InfraErrorHelper(BaseErrorHelper):
	_default = InterpreterError


class InvalidVerbDefinitionError(InterpreterError):
	'''Raised when a invalid Verb definition is found during init'''
	_msg = 'Verb {verb} missing required attribute {attr}'
