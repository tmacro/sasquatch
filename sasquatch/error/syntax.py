from .base import SQError, BaseErrorHelper
from .context import ContextAwareError


class SQSyntaxError(ContextAwareError, SQError):
	_msg = 'invalid syntax'


class SyntaxErrorHelper(BaseErrorHelper):
	@staticmethod
	def throw(cls = SQSyntaxError, **kwargs):
		if 'token' in kwargs:
			token = kwargs.get('token')
			return BaseErrorHelper.throw(cls, **token.context._asdict(), **kwargs)
		if 'ctx' in kwargs and kwargs['ctx'] is not None:
			ctx = kwargs.get('ctx')
			return BaseErrorHelper.throw(cls, **ctx._asdict(), **kwargs)
		BaseErrorHelper.throw(cls, **kwargs)


class MissingVerbError(SQSyntaxError):
	'''Raised when Nouns are found with no attached Verb'''
	_msg = 'Noun <{noun}> has no attached Verb!'

	def __init__(self, **kwargs):
		if 'token' in kwargs:
			token = kwargs.get('token')
			noun = token.value
			if token.keyword is not None:
				noun = '%s=%s'%(token.keyword, noun)
				kwargs['noun'] = noun
		super().__init__(**kwargs)


class UnknownVerbError(SQSyntaxError):
	'''Raised when and unrecognized verb is found'''
	_msg = '{verb} is not a valid Verb!'
	def __init__(self, **kwargs):
		if 'token' in kwargs:
			token = kwargs.get('token')
			kwargs['verb'] = token.name
		super().__init__(**kwargs)


class MissingKeywordError(SQSyntaxError):
	_msg = '{verb} missing required keyword `{keyword}`'


class ExtraKeywordError(SQSyntaxError):
	_msg = '"{verb}" passed extra keyword `{keyword}`'


class MissingPositionalArgumentError(SQSyntaxError):
	_msg = '{verb} missing required keyword `{keyword}`'
	def __init__(self, **kwargs):
		if 'token' in kwargs:
			token = kwargs.get('token')
			kwargs['verb'] = token.name
		super().__init__(**kwargs)


class TooManyArgumentsError(SQSyntaxError):
	_msg = '{verb} takes {takes} arguments but {given} were given'


class ArgumentsOutOfOrderError(SQSyntaxError):
	'''Raised when positional arguments are passed after keyowrd arguments have been used'''
	_msg = 'Positional arguments found after keyword arguments!'
	def __init__(self, **kwargs):
		if 'token' in kwargs:
			token = kwargs.get('token')
			kwargs['noun'] = token.keyword
		super().__init__(**kwargs)

class DuplicateKeywordError(SQSyntaxError):
	'''Raised when two arguments with the same keyword are passed'''
	_msg = '{keyword} passed twice to {verb}'
	def __init__(self, **kwargs):
		if 'token' in kwargs:
			token = kwargs.get('token')
			kwargs['keyword'] = token.keyword
		super().__init__(**kwargs)
