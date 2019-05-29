import os.path
import yaml

from . import lex
from . import parse as _parse
from . import verb
from .verb import VERBS
from ..util.log import Log

_log = Log('grammar')

GRAMMAR_FILE = os.path.dirname(__file__) + '/grammar.yaml'

with open(GRAMMAR_FILE) as grammar_file:
	grammar = yaml.full_load(grammar_file)
	for label, vconf in grammar.items():
		if label.startswith('_'):
			continue
		verb.verb_builder(label, **vconf)


def parse(expr):
	_log.debug('Parsing input to tokens')
	tokens = lex.tokenize(expr)
	_log.debug('Found tokens %s'%tokens)
	_log.debug('Parsing tokens to verbs')
	verbs = list(_parse.parse(tokens, VERBS))
	_log.debug('Found verbs %s'%verbs)
	return verbs
