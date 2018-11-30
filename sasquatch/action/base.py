import sys
from ..pipe import StubResult, ReturnResult
from ..error.syntax import MissingKeywordError
from ..error.syntax import SyntaxErrorHelper as error

import types
ACTIONS = {}

def add_action(cls):
	ACTIONS[cls._name] = cls
	return cls

class Action:
	def __init__(self, *args, **kwargs):
		self._verb = self
		self.__keywords = None
		super().__init__(*args, **kwargs)

	def _collect_keywords(self, value):
		from_value = value.args(*self.wants)
		from_value.update(self._kwargs)
		try:
			self._check_kwargs(
				strict=True,
				**{ k: v for k, v in from_value.items() if v is not None }
			)
		except MissingKeywordError as e:
			error.throw(MissingKeywordError, verb=self._symbol, keyword=e._fmt_args['keyword'], ctx=self._context)
			# verb=self._symbol, keyword=key, ctx=kwargs[key].context
		return from_value

	def _extract_from_noun(self, **kwargs):
		extracted = { k: v.value for k, v in kwargs.items() if v is not None }
		extracted.update((k, v) for k, v in kwargs.items() if v is None)
		return extracted

	def _process(self, **kwargs):
		'''
			Is passed a result and is expected to return a result
		'''
		return StubResult(kwargs)

	def _finish(self):
		return None

	def do(self, results):
		'''
			Expects to be passed a iterable of results
			and to yield a result for each
		'''
		for result in results:
			kwargs = self._collect_keywords(result)
			value = self._process(**kwargs)
			if value is not None:
				if isinstance(value, types.GeneratorType):
					for v in value:
						yield v
				else:
					yield value
		value = self._finish()
		if value is not None:
			yield value

@add_action
class FinalAction(Action):
	'''This Action is used for an implicit ending verb that produces a return code'''
	_name = '_final'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__return_code = 0

	def _collect_keywords(self, value):
		print(value._repr())
		return super()._collect_keywords(value)

	def _process(self, **kwargs):
		if 'return_code' in kwargs and kwargs['return_code'] is not None:
			self.__return_code = kwargs.get('return_code')
		return None

	def _finish(self):
		return ReturnResult({'_return_code': self.__return_code})

	def do(self, results):
		return super().do(results)
