from itertools import chain
from ..error import InvalidVerbError, ExtraKeyword, MissingArgument, TooManyArguments, MissingKeyword
from ..util.log import Log

_log = Log('grammar.verb')

VERBS = {}

def add_verb(cls):
	VERBS[cls._symbol] = cls



# The base class for all verbs
class BaseVerb:
	# _hard_required  - required everytime, can't be built from input
	# _soft_required  - required everytime, can be built from input
	# _optional       - not required - can't be built from input
	_hard_required = []
	_soft_required = []
	_optional = []
	# Order keywords will be matched to positional arguments
	_positional_order = None

	def __init__(self, *args, **kwargs):
		if self._positional_order is None:
			self._positional_order = self._soft_required[:]
		self._check_args(*args)
		kwargs.update({k:v.value for k, v in self._resolve_positional(*args)})
		self._check_kwargs(**kwargs)
		self._kwargs = kwargs

	def _check_args(self, *args):
		if len(args) > len(self._positional_order):
			raise TooManyArguments(self._optional, self._positional_order)
		return True

	def _check_kwargs(self, strict=False, **kwargs):
		# Build our lists of valid keywords
		required = self._hard_required[:]
		optional = self._optional[:]
		# _soft_required becomes hard if strict is True
		# otherwise _ soft_required is optional
		if strict:
			required += self._soft_required[:]
		else:
			optional += self._soft_required[:]
		# Iterate over our keys removing them from our
		# lists if they're there
		for key in kwargs.keys():
			if key in required:
				required.remove(key)
			elif key in optional:
				optional.remove(key)
			else: # raise an exception if it's extra
				raise ExtraKeyword(key, verb=self._symbol, nouns=kwargs)
		# if there are any left raise an exception
		if required:
			raise MissingKeyword(', '.join(required))
		return True

	def _resolve_positional(self, *args, position = 0):
		if not self._check_args(*args):
			raise Exception
		return list(zip(self._positional_order[position:], args))

	def __repr__(self):
		tmpl = '<sasquatch.grammar.verb.%s %s>'
		nouns = ' '.join('%s=%s'%(k,v) for k, v in self._kwargs.items())
		return tmpl%(self._symbol.upper(), nouns)



	@property
	def has(self):
		return list(self._kwargs.keys())

	@property
	def needs(self):
		return list(chain(
			self._hard_required,
			self._soft_required,
		))

	@property
	def wants(self):
		return list(chain(
			self._needs,
			self._optional
		))

	@property
	def missing(self):
		has = self.has
		return list(filter(lambda k: k not in has, self.needs))


def get_or_raise(dikt, key, err):
	if key not in dikt:
		raise err
	return dikt.get(key)

_builder_log = Log('grammar.verb.builder')
def verb_builder(name, **kwargs):
	_builder_log.debug('Loading verb %s'%name)
	symbol = get_or_raise(kwargs, 'symbol', InvalidVerbError(name, 'symbol'))
	desc = kwargs.get('desc', None)
	hard_required = kwargs.get('hard_required', [])
	soft_required = kwargs.get('soft_required', [])
	optional = kwargs.get('optional', [])
	positional_order = kwargs.get('positional_order', None)

	class _Verb(BaseVerb):
		_symbol = symbol
		_desc = desc
		__doc__ = desc
		_hard_required = hard_required
		_soft_required = soft_required
		_optional = optional
		_positional_order = positional_order
	_Verb.__name__ = name
	_Verb.__qualname__= 'grammar.verb.%s'%(name.upper())
	add_verb(_Verb)



# @add_verb
# class LS(BaseVerb):
# 	_optional = ['bucket', 'key']
# 	_positional_order = ['bucket', 'key']
# 	_symbol = 'ls'


# @add_verb
# class HEAD(BaseVerb):
# 	'''Retrieve info for an object'''
# 	_symbol = 'head'
# 	_soft_required = ['bucket', 'key']
# 	_optional = ['version_id']
# 	_positional_order = ['bucket', 'key']




# @add_verb
# class GET(BaseVerb):
# 	'''Get an object from storage'''
# 	_symbol = 'get'
# 	_soft_required = ['bucket', 'key']
# 	_optional = ['version_id']
	# _positional_order = ['bucket', 'key']
