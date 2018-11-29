from conftest import *
import pytest
import sasquatch
import sasquatch.grammar.lex
from sasquatch.grammar.lex import VerbT, NounT

GRAMMAR_ANWSER_FILE = os.path.dirname(__file__) + '/../grammar/lex.yaml'

ANSWERS = load_grammar(GRAMMAR_ANWSER_FILE)

QA = list(zip(VALID_GRAMMAR, ANSWERS['valid']))
@pytest.fixture(scope='session', params=QA)
def qa(request):
	input_text, answer = request.param
	return make_fd(input_text), answer



TypeMapping = {
	'Verb' : VerbT,
	'Noun' : NounT
}

def test_tokens(qa):
	grammar, answers = qa
	tokens = sasquatch.grammar.lex.tokenize(grammar)
	for token, answer in zip(tokens, answers):
		for key, value in answer.items():
			if key == 'type':
				assert isinstance(token, TypeMapping[value])
				continue
			assert getattr(token, key) == value
