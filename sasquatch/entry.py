import os.path
import sys

from .eval import eval_expr
from .util import log
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
		print(err)
		if log.DEBUG:
			raise
		sys.exit(-1)

def main():
	args = parse_args()
	fd = FakeSTDIN(args['script'])
	eval_expr(fd)
