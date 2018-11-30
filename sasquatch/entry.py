import os.path
import sys

from .eval import eval_expr
from .util import log
from .util.conv import FakeSTDIN
from .util.conf import config


def entry():
	try:
		main()
	except Exception as err:
		print(err)
		# if log.DEBUG:
		raise
		sys.exit(-1)

def print_version():
	print('%s %s'%(config.meta.name, config.meta.version))

def main():
	if config.runtime.version_flag:
		print_version()
		sys.exit(0)
	elif config.runtime.file:
		with open(config.runtime.file) as script_file:
			fd = FakeSTDIN(script_file.read())
			fd.name = config.runtime.file
	elif config.runtime.script:
		fd = FakeSTDIN(config.runtime.script)
	else:
		fd = sys.stdin
	sys.exit(eval_expr(fd).get('return_code', 0))
