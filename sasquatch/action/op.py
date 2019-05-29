from pathlib import PosixPath

from ..pipe import HeadResult, GetResult
from ..s3 import api as s3api
from .base import Action, add_action
from ..error.exec import ExecErrorHelper as error
from ..error.exec import InvalidFilePathError

@add_action
class HeadAction(Action):
	_name = 'head'
	def _process(self, **kwargs):
		kwargs = self._extract_from_noun(**kwargs)
		bucket = kwargs['bucket']
		key = kwargs['key']
		res = s3api.head(**kwargs)
		return HeadResult(
			dict(
				_key=key,
				_bucket=bucket,
				**res
			)
		)

_CHUNK_SIZE = 1024 * 1024 * 5 # 5MB
@add_action
class GetAction(Action):
	_name = 'get'
	def _process(self, **kwargs):
		keywords = self._extract_from_noun(**kwargs)
		bucket = keywords['bucket']
		key = keywords['key']
		version_id = keywords.get('version_id', None)
		filename = keywords.get('filename', None)
		obj = self.__get_obj(bucket, key, version_id)
		if obj is not None and 'Body' in obj:
			path = self.__gen_filename(key, version_id, filename)
			if path is None:
				error.throw(InvalidFilePathError, ctx=kwargs['filename'].context, filepath=filename)
			self.__write_obj(obj['Body'], path)
			return GetResult(
				dict(
					_key=key,
					_bucket=bucket,
					_filename=filename,
					**obj
				)
			)

	def __get_obj(self, bucket, key, version_id=None):
		res  = s3api.get(bucket=bucket, key=key, version_id=version_id)
		if not res.get('DeleteMarker', False):
			return res

	def __gen_filename(self, key, version_id=None, filename=None):
		if filename is not None:
			filename = PosixPath(filename).resolve()
			if filename.is_file():
				return filename.as_posix()
			elif filename.is_dir() and filename.exists():
				basepath = filename
			else:
				return None
		else:
			basepath = PosixPath.cwd()
		leaf = key
		if version_id is not None:
			leaf = '%s-%s'%(leaf, version_id)
		return basepath.joinpath(leaf).as_posix()

	def __write_obj(self, obj, filename):
		with open(filename, 'wb') as objfile:
			for chunk in obj.iter_chunks(_CHUNK_SIZE):
				objfile.write(chunk)
