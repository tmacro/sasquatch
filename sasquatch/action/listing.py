from .base import Action, add_action
from ..s3 import api as s3api
from ..pipe import BucketResult, ObjectResult, ObjectVersionResult
from itertools import chain

@add_action
class ListAction(Action):
	_name = 'ls'

	def __list_buckets(self, **kwargs):
		for page in s3api.ls(**kwargs):
			for bucket in page['Buckets']:
				yield dict(**bucket)

	def _list_objects(self, **kwargs):
		kwargs = self._extract_from_noun(**kwargs)
		bucket = kwargs.get('bucket')
		for page in s3api.ls(**kwargs):
			for obj in page['Contents']:
				yield dict(_bucket=bucket, **obj)

	def _process(self, **kwargs):
		if kwargs.get('bucket', None) is not None:
			result_type = ObjectResult
			result_func = self._list_objects
		else:
			result_type = BucketResult
			result_func = self.__list_buckets
		for result in result_func(**kwargs):
			yield result_type(result, ctx=self._context)


@add_action
class ListVersionAction(Action):
	_name = 'lv'

	def _process(self, **kwargs):
		kwargs = self._extract_from_noun(**kwargs)
		bucket = kwargs.get('bucket')
		for page in s3api.lv(**kwargs):
			for version in chain(
				page['Versions'] if 'Versions' in page else [],
				page['DeleteMarkers'] if 'DeleteMarkers' in page else []):
				version['_bucket'] = bucket
				yield ObjectVersionResult(version, ctx=self._context)
