from enum import Enum
from collections.abc import ABCMeta
from .error.exec import MissingKeywordError
from .error.exec import ExecErrorHelper as error

class ResultTypes(Enum):
	BUCKET = 1
	OBJECT = 2

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
		return { k:self._get_arg(k) for k in args }

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
