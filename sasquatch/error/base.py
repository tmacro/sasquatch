'''
Module for base error class
'''


class BaseError(Exception):
	_msg = "There's been an error!"

	def __init__(self, **kwargs):
		self._fmt_args = kwargs
		super().__init__(self._msg.format(**kwargs))

	def __repr__(self):
		return '%s: %s'%(
			self.__class__.__name__,
			self._msg.format(**self._fmt_args)
		)

	def __str__(self):
		return self.__repr__()


class SQError(BaseError):
	'''Root error for all Sasquatch exceptions'''


class BaseErrorHelper:
	_default = SQError
	@classmethod
	def throw(cls, err = None, **kwargs):
		if err is None and cls._default is not None:
			err = cls._default
		raise err(**kwargs)
