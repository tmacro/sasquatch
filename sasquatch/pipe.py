from .error.exec import MissingKeywordError
from .error.exec import ExecErrorHelper as error
from .grammar.lex import NounT

class BaseResult:
	_mapping = {}
	def __init__(self, data):
		self._data = data

	def _convert_arg(self, arg, value):
		convert_func = getattr(self, '_convert_kw_%s'%arg, None)
		if convert_func is not None:
			return convert_func(value)
		return value

	def _get_arg(self, arg):
		key = self._mapping.get(arg)
		if key is None:
			return None
		value = self._data.get(key)
		return self._convert_arg(arg, value)

	def args(self, *args):
		return { k: self._get_arg(k) for k in args }

class ContextResult(BaseResult):
	def __init__(self, data, ctx=None):
		super().__init__(data)
		self._context = ctx

class NounResult(ContextResult):
	def _convert_arg(self, arg, value):
		value = super()._convert_arg(arg, value)
		return NounT(None, value, self._context)

class StubResult(NounResult):
	'''For use with beginning verb'''

class BucketResult(BaseResult):
	_mapping = {
		'bucket': 'Name'
	}

class ObjectResult(BaseResult):
	_mapping = {
		'bucket': '_bucket',
		'key': 'Key'
	}

class HeadResult(BaseResult):
	_mapping = {
		'bucket': '_bucket',
		'key': '_key',
		'version_id': 'VersionId'
	}

class ReturnResult(BaseResult):
	_mapping = {
		'return_code': '_return_code'
	}
