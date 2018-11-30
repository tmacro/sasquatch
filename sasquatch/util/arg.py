import argparse
from collections import namedtuple
from collections.abc import Iterable, Mapping
import six
from itertools import chain, zip_longest

def recurse_update(orig, new):
	'''
	Given a nested dict/list combo, walk each and update orig with new,
	overwiting keys, and positions
	'''
	if orig is None:
		return new
	elif new is None:
		return orig
	elif type(orig) != type(new):
		return new
	# Check for strings specifically because they cause problems with lists
	elif isinstance(orig, six.string_types) and isinstance(new, six.string_types):
		return new
	elif isinstance(orig, Mapping) and isinstance(new, Mapping):
		return {
			k: recurse_update(
				orig.get(k),
				new.get(k)
			) for k in set(
				chain(
					orig.keys(),
					new.keys()
				)
			)
		}
	elif isinstance(orig, Iterable) and isinstance(new, Iterable):
		return [recurse_update(o, n) for o, n in zip_longest(orig, new)]
	return new

class Undefined:
	'''Simple placeholder for nonexistent config values, because None can be a valid value'''

class BaseAction(argparse.Action):
	def __init__(self, option_strings, dest, **kwargs):
		dest, self._path = self._get_level(dest)
		super().__init__(option_strings, dest, **kwargs)

	def _get_level(self, path):
		parts = path.split('.')
		return parts[0], '.'.join(parts[1:])

	def _build_value(self, key, value):
		if not key:
			return value
		toplvl, left = self._get_level(key)
		return {toplvl: self._build_value(left, value)}

	def __call__(self, parser, namespace, value, option_string=None):
		if value is Undefined:
			return None
		opt_value = self._build_value(self._path, value)
		if hasattr(namespace, self.dest):
			updated = recurse_update(getattr(namespace, self.dest), opt_value)
		else:
			updated = opt_value
		setattr(namespace, self.dest, updated)

class CallbackAction(BaseAction):
	def __init__(self, *args, func = None, **kwargs):
		self._func = func
		super().__init__(*args, **kwargs)

	def __call__(self, parser, namespace, value, option_string=None):
		super().__call__(parser, namespace, self._func(value))


OPTIONS = []

Option = namedtuple('Option', ['flags', 'func', 'kwargs'])

def option(*args, **kwargs):
	def inner(f):
		if 'default' not in kwargs:
			kwargs['default'] = Undefined
		OPTIONS.append(Option(args, f, kwargs))
		return f
	return inner

def flag(*args, **kwargs):
	def inner(f):
		if 'default' not in kwargs:
			kwargs['default'] = Undefined
		kwargs['nargs'] = 0
		OPTIONS.append(Option(args, f, kwargs))
		return f
	return inner


def parse_args(name=None, desc=None):
	parser = argparse.ArgumentParser(prog=name, description=desc)
	for option in OPTIONS:
		parser.add_argument(*option.flags, func=option.func, **option.kwargs, action=CallbackAction)
	return { k: v for k, v in vars(parser.parse_args()).items() if v is not Undefined }
