from . import grammar
from .util.log import Log
from .pipe import StubResult
from .grammar.verb import VERBS
_log = Log('eval')

CHARSET_REGEX = r'[a-zA-Z0-9./=:|]+'


class Interpreter:
	def __init__(self):
		self._last_result = None

	def _execute(self, word):
		if self._last_result is None:
			return word.do([StubResult({})])
		else:
			return word.do(self._last_result)

	def eval(self, expression):
		for word in grammar.parse(expression):
			self._last_result = self._execute(word)
		_end = VERBS['_end']()
		return next(self._execute(_end)).args('return_code')

def eval_expr(expr):
	return Interpreter().eval(expr)
