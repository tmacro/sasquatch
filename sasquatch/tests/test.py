from .. import eval as sqeval
from ..error import SQError
import os.path

GRAMMAR_TEST_FILE = os.path.dirname(__file__) + '/test_grammar.txt'

def run_tests():
	with open(GRAMMAR_TEST_FILE) as test_input:
		for line in test_input:
			if not line.strip() or line.startswith('#'):
				continue
			print('"%s"'%line.strip())
			try:
				print(sqeval.eval_expr(line.strip()))
			except SQError as err:
				if err._nouns is not None:
					print(err._nouns)
				if err._verb is not None:
					print(err._verb)
				raise
