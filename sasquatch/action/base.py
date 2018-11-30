import sys
from ..pipe import StubResult, ReturnResult
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
		return from_value

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

	def _process(self, **kwargs):
		if 'return_code' in kwargs and kwargs['return_code'] is not None:
			self.__return_code = kwargs.get('return_code')
		return None

	def _finish(self):
		return ReturnResult({'_return_code': self.__return_code})



@add_action
class ListAction(Action):
	_name = 'ls'
