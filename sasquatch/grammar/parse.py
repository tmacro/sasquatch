from ..util.fsm import State, Actor
from ..util.safe import firstel
from .lex import VerbT, NounT
from .. import error as sqerror

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
				raise Exception
	if verb is not None:
		yield verb, nouns



def parse(tokens, verbs):
	for position, (verb, nouns) in enumerate(find_chunk(tokens)):
		if not verb.name in verbs:
			raise sqerror.SyntaxError(sqerror.SQSyntaxError ,verb.name, position=position)
			# raise sqerror.SQSyntaxError(verb.name, position = position)
		verb_cls = verbs[verb.name]
		positional = []
		keyword = []
		for noun in nouns:
			if noun.keyword is None:
				if keyword: # If keyword args already exist
					raise sqerror.SyntaxError(sqerror.SQSyntaxError, noun.value, verb=verb_cls, position=position)
					# raise sqerror.SQSyntaxError(noun.value, position = position)
				positional.append(noun)
			else:
				keyword.append(noun)
		keyword = {n.keyword:n.value for n in keyword}
		yield verb_cls(*positional, **keyword)
