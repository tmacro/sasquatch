


class BaseError(Exception):
	_msg = "There's been an error!"
	def __init__(self, *args, verb = None, nouns = None):
		self._nouns = nouns
		self._verb = verb
		super().__init__(self._msg%args)




class SQError(BaseError):
	'''Root error for all Sasquatch exceptions'''

class MissingArgument(SQError):
	_msg = '%s arguments specified, %s arguments are required'

class TooManyArguments(SQError):
	_msg = '%s arguments specified, %s arguments are required'

class MissingKeyword(SQError):
	_msg = 'Required keyword %s missing!'

class ExtraKeyword(SQError):
	_msg = 'Extra or duplicate keyword found %s'

class SQSyntaxError(SQError):
	_msg = 'Invalid syntax found at token %s'

class InvalidVerbError(SQError):
	_msg = 'Verb %s missing required attribute %s'
