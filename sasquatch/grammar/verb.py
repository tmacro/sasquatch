from itertools import chain
from ..error.infra import InvalidVerbDefinitionError
from ..error.infra import InfraErrorHelper as infraerrors
from ..error.syntax import SyntaxErrorHelper as stxerrors
from ..error.syntax import MissingKeywordError, MissingPositionalArgumentError, ExtraKeywordError, TooManyArgumentsError
from ..util.log import Log
from ..action import ACTIONS
from ..action.base import Action

_log = Log('grammar.verb')

VERBS = {}

def add_verb(cls):
	VERBS[cls._symbol] = cls
	return cls



# The base class for all verbs
class BaseVerb:
	_symbol = None
	_desc = None
	# _hard_required  - required everytime, can't be built from input
	# _soft_required  - required everytime, can be built from input
	# _optional       - not required - can be built from input
	_hard_required = []
	_soft_required = []
	_optional = []
	# Order keywords will be matched to positional arguments
	_positional_order = None

	def __init__(self, *args, ctx=None, **kwargs):
		self._context = ctx
		if self._positional_order is None:
			self._positional_order = self._soft_required[:]
		self._check_args(*args)
		kwargs.update(self._resolve_positional(*args))
		self._check_kwargs(**kwargs)
		self._kwargs = kwargs

	def _check_args(self, *args):
		takes = len(self._positional_order)
		given = len(args)
		if given > takes:
			stxerrors.throw(TooManyArgumentsError, verb=self._symbol, takes=takes, given=given, ctx=args[-1].context)
		return True

	def _check_kwargs(self, strict=False, **kwargs):
		# Build our lists of valid keywords
		required = self._hard_required[:]
		optional = self._optional[:]
		# _soft_required becomes hard if strict is True
		# otherwise _soft_required is optional
		if strict:
			required += self._soft_required[:]
		else:
			optional += self._soft_required[:]
		# Iterate over our keys removing them from our
		# lists if they're there
		last_key = None
		for key in kwargs.keys():
			if key in required:
				required.remove(key)
			elif key in optional:
				optional.remove(key)
			else: # raise an exception if it's extra
				stxerrors.throw(ExtraKeywordError, verb=self._symbol, keyword=key, ctx=kwargs[key].context)
			last_key = key
		# if there are any left raise an exception
		if required:
			if last_key:
				ctx = kwargs[last_key].context
			else:
				ctx = self._context
			stxerrors.throw(MissingKeywordError, verb=self._symbol, keyword=required[0], ctx=ctx)

		return True

	def _resolve_positional(self, *args, position = 0):
		if not self._check_args(*args):
			raise Exception
		return { k:v for k, v in zip(self._positional_order[position:], args) }

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
			self.needs,
			self._optional
		))

	@property
	def missing(self):
		has = self.has
		return list(filter(lambda k: k not in has, self.needs))

	@property
	def keywords(self):
		return { k: v for k, v in self._kwargs if v is not None}


def get_or_raise(dikt, key, err):
	if key not in dikt:
		raise err
	return dikt.get(key)

def get_s3_action(name):
	return ACTIONS.get(name, Action)

_builder_log = Log('grammar.verb.builder')
def verb_builder(name, **kwargs):
	_builder_log.debug('Loading verb %s'%name)
	if not 'symbol'in kwargs:
		infraerrors.throw(InvalidVerbDefinitionError, verb=name, attr='symbol')
	symbol = kwargs.get('symbol')
	desc = kwargs.get('desc', None)
	hard_required = kwargs.get('hard_required', [])
	soft_required = kwargs.get('soft_required', [])
	optional = kwargs.get('optional', [])
	positional_order = kwargs.get('positional_order', None)
	action_name = kwargs.get('action', None)
	action = get_s3_action(action_name)
	# if action is None:
	# 	infraerrors.throw(InvalidVerbDefinitionError, verb=name, action=action_name)

	class _Verb(action, BaseVerb):
		_symbol = symbol
		_desc = desc
		__doc__ = desc
		_hard_required = hard_required
		_soft_required = soft_required
		_optional = optional
		_positional_order = positional_order

	_Verb.__name__ = name
	_Verb.__qualname__= '%s'%(name.upper())
	add_verb(_Verb)

@add_verb
class EndingVerb(ACTIONS['_final'], BaseVerb):
	_symbol = '_end'
	_optional = ['return_code']
