import argparse
import sys
from collections import OrderedDict

OPTIONS = []


def option(*args, **kwargs):
	def dec(f):
		OPTIONS.append((kwargs, f))
		return f
	return dec

@option('-v', '--version')
def version(*args, **kwargs):
	from .__init__ import __version__
	print(__version__)
	sys.exit(0)


def build_parser(name, desc = None):
	parser = argparse.ArgumentParser(prog=name, description=desc)
	for args, kwargs in OPTIONS:
		parser.add_argument(*args, **kwargs)
	return parser

class CallbackAction(argparse.Action):
	def __init__(self, func, *args, **kwargs):
		self._func = func
		super().__init__(*args, **kwargs)

	def __call__(self, parser, namespace, values, option_string=None):
		self._func(namespace, values, option_string)
		# setattr(namespace, self.dest, values)
