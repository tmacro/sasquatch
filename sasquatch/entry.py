import os.path
import sys

from .eval import eval_expr
from .util import log
from .util.conv import FakeSTDIN
from .util.conf import config

_log = log.Log('entry')

def entry():
	try:
		main()
	except KeyboardInterrupt:
		print(' Received SIGINT', file=sys.stderr)
		sys.exit(0)
	except Exception as err:
		print(err)
		_log.debug(err)
		if log.DEBUG:
			_log.exception(err)
		sys.exit(-1)

def main():
	if config.runtime.version_flag:
		print_version()
		sys.exit(0)
	elif config.runtime.file:
		_log.debug('Reading script from %s'%config.runtime.file)
		with open(config.runtime.file) as script_file:
			fd = FakeSTDIN(script_file.read())
			fd.name = config.runtime.file
	elif config.runtime.script:
		_log.debug('Reading script from cli')
		fd = FakeSTDIN(config.runtime.script)
	else:
		_log.debug('Reading script from STDIN')
		fd = sys.stdin
	sys.exit(eval_expr(fd).get('return_code', 0))
