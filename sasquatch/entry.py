from .eval import eval_expr
import sys
import os.path
from .tests import test

USAGE='''Not enough arguments provided!
Usage: %s '<expr>\''''

def parse_args():
	if len(sys.argv) < 2:
		raise Exception(USAGE%os.path.basename(sys.argv[0]))
	return dict(script=sys.argv[1])


def main():
	# args = parse_args()
	# eval_expr(args['script'])
	test.run_tests()
