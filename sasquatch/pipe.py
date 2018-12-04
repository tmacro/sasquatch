from .error.exec import MissingKeywordError
from .error.exec import ExecErrorHelper as error
from .grammar.lex import NounT
from .const import DATETIME_FMT

class BaseResult:
	_mapping = {}
	def __init__(self, data):
		self._data = data

	def __repr__(self):
		tmpl = '<sasquatch.pipe.action.%s %s>'
		nouns = ' '.join('%s=%s'%(k,v) for k, v in self._data.items())
		return tmpl%(self.__class__.__name__, nouns)


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
	pass

class BucketResult(NounResult):
	_mapping = {
		'bucket': 'Name'
	}
	def _repr(self):
		dt = self._data['CreationDate'].strftime(DATETIME_FMT)
		return '{date} {name}'.format(date=dt, name=self._data['Name'])

class ObjectResult(NounResult):
	_mapping = {
		'bucket': '_bucket',
		'key': 'Key'
	}
	def _repr(self):
		return '{LastModified} {Size:>10} {Key}'.format(**self._data)

class ObjectVersionResult(NounResult):
	_mapping = {
		'bucket': '_bucket',
		'key': 'Key',
		'version_id': 'VersionId'
	}
	def _repr(self):
		size = self._data.get('Size', 'DM')
		return '{LastModified} {_size:>10} {VersionId} {Key}'.format(_size = size, **self._data)


class HeadResult(NounResult):
	_tmpl = '''{\n%s\n}'''
	_mapping = {
		'bucket': '_bucket',
		'key': '_key',
		'version_id': 'VersionId'
	}

	def _repr(self):
		return self._tmpl%(',\n'.join('    "%s": "%s"'%(k,v) for k,v in self._data.items() if k != 'ResponseMetadata' and not k.startswith('_')))
		# return '{LastModified} {ContentLength} {_key}'.format(**self._data)

class ReturnResult(BaseResult):
	_mapping = {
		'return_code': '_return_code'
	}
