



class ErrorMixin:
	'''Mixin to provide context aware error messages to the user'''

	def __init__(self *args, **kwargs):
		self._filename = kwargs.get('filename')
		self._lineno = kwargs.get('lineno')
		self._text = kwargs.get('text')
		self._offset = kwargs.get('ooffset')
		self._msg = kwargs.get('msg')




































class BaseError(Exception):
	_msg = "There's been an error!"
	def __init__(self, *args, verb = None, nouns = None, position = None):
		self._args = args
		self._nouns = nouns
		self._verb = verb
		self._position = position
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
	_msg = 'Unexpected token "%s"!'

class InvalidVerbError(SQError):
	_msg = 'Verb %s missing required attribute %s'

def SyntaxError(err, *args, verb = None, nouns = [], position = None):
	kwargs = dict()
	if verb:
		kwargs['verb'] = verb,
	if nouns:
		kwargs['nouns'] = nouns
	if position is not None:
		kwargs['position'] = position
	return err(*args, **kwargs)

VERB_TPL = 'Verb: %s'
POS_TPL = 'Position: %s'
NOUN_TPL = '%s=%s'

def ReportError(err):
	report = []
	report.append(err._msg%err._args)
	if err._verb:
		report.append(VERB_TPL%err._verb)
	if err._position is not None:
		report.append(POS_TPL%err._position)
	if err._nouns:
		report.append(' '.join([NOUN_TPL%(n.keyword, n.value) for n in err._nouns]))
	return '%s: %s'%(err.__class__.__name__, ' '.join(report))
