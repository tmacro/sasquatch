from .base import SQError, BaseErrorHelper


class UserError(SQError):
	'''Error raised when the user passes invalid non-code input'''

class UserErrorHelper(BaseErrorHelper):
	_default = UserError

class UnknownProfileError(SQError):
	'''Raised when the specified profile does not exist'''
	_msg = 'Profile {profile} can not be located!'
