from ..util.fsm import State, Actor
from ..util.conv import firstel
from .lex import VerbT, NounT
from ..error.syntax import SyntaxErrorHelper as errors
from ..error.syntax import MissingVerbError, UnknownVerbError, ArgumentsOutOfOrderError

def find_chunk(tokens):
	verb = None
	nouns = []
	for token in tokens:
		if isinstance(token, VerbT):
			if verb is not None:
				yield verb, nouns
			verb = token
			nouns = []
		else:
			if verb	is not None:
				nouns.append(token)
			else:
				errors.throw(MissingVerbError, token=token)
	if verb is not None:
		yield verb, nouns



def parse(tokens, verbs):
	for position, (verb, nouns) in enumerate(find_chunk(tokens)):
		if not verb.name in verbs:
			errors.throw(UnknownVerbError, token=verb)
		verb_cls = verbs[verb.name]
		positional = []
		keyword = []
		for noun in nouns:
			if noun.keyword is None:
				if keyword: # If keyword args already exist
					errors.throw(ArgumentsOutOfOrderError, token=noun)
				positional.append(noun)
			else:
				keyword.append(noun)
		keyword = {n.keyword:n for n in keyword}
		yield verb_cls(*positional, ctx=verb.context, **keyword)


def parserv2(tokens, verbs):
	pass
