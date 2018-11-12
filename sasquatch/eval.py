from pprint import pprint
from . import grammar

CHARSET_REGEX = r'[a-zA-Z0-9./=:|]+'
WORD_REGEX = ''






def eval_expr(expr):
	words = grammar.parse(expr)
	print(words)
