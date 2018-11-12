import os.path
import yaml

from . import lex
from . import parse as _parse
from . import verb
from .verb import VERBS

GRAMMAR_FILE = os.path.dirname(__file__) + '/grammar.yaml'

with open(GRAMMAR_FILE) as grammar_file:
	grammar = yaml.load(grammar_file)
	for label, vconf in grammar.items():
		if label.startswith('_'):
			continue
		verb.verb_builder(label, **vconf)

print(list(v._positional_order for _, v in VERBS.items()))

def parse(expr):
	tokens = lex.tokenize(expr)
	verbs = list(_parse.parse(tokens, VERBS))
	print(verbs)
