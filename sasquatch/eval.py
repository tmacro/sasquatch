from pprint import pprint
from . import grammar
from .util.log import Log

_log = Log('eval')

CHARSET_REGEX = r'[a-zA-Z0-9./=:|]+'

def eval_expr(expr):
	words = grammar.parse(expr)
	_log.debug('Parsed input to %s'%(words))
	return words
