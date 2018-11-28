import os.path

import pytest
import yaml

# from . import util
# from ..eval import eval_expr
# from ..util.conv import FakeSTDIN
from sasquatch.util.conv import FakeSTDIN
GRAMMAR_TEST_FILE = os.path.dirname(__file__) + '/grammar/grammar.yaml'

def load_grammar(filename = GRAMMAR_TEST_FILE):
	with open(filename) as test_input:
		grammar = yaml.load(test_input)
		return grammar

GRAMMAR = load_grammar()
VALID_GRAMMAR = GRAMMAR['valid']
INVALID_GRAMMAR = GRAMMAR['invalid']

def make_fd(string):
	return FakeSTDIN(string)

@pytest.fixture(scope='session', params=GRAMMAR['valid'])
def valid_grammar(request):
	return make_fd(request.param)
