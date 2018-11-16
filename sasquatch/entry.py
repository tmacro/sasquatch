from .eval import eval_expr
import sys
import os.path
from .tests import test
from .error import SQError, SQSyntaxError, ReportError
from .util.conv import FakeSTDIN
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
		# if isinstance(err, SQSyntaxError):
		# 	print(ReportError(err))
		# elif isinstance(err, SQError):
		# 	print(err)
		# sys.exit(1)
		raise

def main():
	args = parse_args()
	fd = FakeSTDIN(args['script'])
	eval_expr(fd)
	# test.run_tests()
