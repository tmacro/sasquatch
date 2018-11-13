from .eval import eval_expr
import sys
import os.path
from .tests import test
from .error import SQError, SQSyntaxError, ReportError

USAGE='''Not enough arguments provided!
Usage: %s '<expr>\''''

def parse_args():
	if len(sys.argv) < 2:
		raise Exception(USAGE%os.path.basename(sys.argv[0]))
	return dict(script=sys.argv[1])


def entry():
	try:
		main()
	except Exception as err:
		if isinstance(err, SQSyntaxError):
			print(ReportError(err))
		elif isinstance(err, SQError):
			pass
		sys.exit(1)

def main():
	args = parse_args()
	eval_expr(args['script'])
	# test.run_tests()
