from ..util.conv import firstel
from .lex import VerbT, NounT
from ..error.syntax import SyntaxErrorHelper as errors
from ..error.syntax import MissingVerbError, UnknownVerbError, ArgumentsOutOfOrderError, DuplicateKeywordError

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


# The sq language only consists of two different symbols (Verbs & Nouns)
# and has no concept of "reserved words" so parsing is straighforward.
# Since Nouns must have a preceding Verb we simply iterate over our tokens
# grouping Verbs and their following Nouns, rasing an Exception if
# we find a nonexistent Verb or Nouns without a Verb.
def parse(tokens, verbs):
	for position, (verb, nouns) in enumerate(find_chunk(tokens)):
		if not verb.name in verbs:
			errors.throw(UnknownVerbError, token=verb)
		verb_cls = verbs[verb.name]
		positional = []
		keyword = {}
		for noun in nouns:
			if noun.keyword is None: # If the noun is positional
				if keyword: # If keyword args already exist
					errors.throw(ArgumentsOutOfOrderError, token=noun)
				positional.append(noun)
			else: # Its a keyword arg
				if noun.keyword in keyword: # Its its already been passed
					errors.throw(DuplicateKeywordError, token=noun, verb=verb.name)
				keyword[noun.keyword] = noun
		# keyword = {n.keyword:n for n in keyword}
		yield verb_cls(*positional, ctx=verb.context, **keyword)
