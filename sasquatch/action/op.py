from .base import Action, add_action
from ..s3 import api as s3api
from ..pipe import HeadResult

@add_action
class HeadAction(Action):
	_name = 'head'
	def _process(self, **kwargs):
		kwargs = self._extract_from_noun(**kwargs)
		res = s3api.head(**kwargs)
		bucket = kwargs['bucket']
		key = kwargs['key']
		return HeadResult(
			dict(
				_key=key,
				_bucket=bucket,
				**res
			)
		)
