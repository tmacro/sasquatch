from .base import Action, add_action
from ..s3 import api as s3api
import re


class BaseFilter(Action):
	def _process(self, **kwargs):
		return True

	def do(self, results):
		for result in results:
			kwargs = self._collect_keywords(result)
			if self._process(**kwargs):
				yield result


@add_action
class GrepAction(BaseFilter):
	_name = 'gr'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		compiled = re.compile(self._kwargs['regex'].value)
		replaced = self._kwargs['regex']._replace(value=compiled)
		self._kwargs['regex'] = replaced

	def _process(self, **kwargs):
		kwargs = self._extract_from_noun(**kwargs)
		if kwargs['regex'].search(kwargs['key']):
			return True
		return False
