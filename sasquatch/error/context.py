from .base import BaseErrorHelper

'''
Module for implementing content awre error messages for sasquatch
'''

ERROR_TMPL='''
File "{filename}", line {lineno}, col {offset}
  {text}
  ^
{msg}
'''.strip()


class ContextAwareError:
	'''Mixin to provide context aware error messages to the user'''

	_tmpl = ERROR_TMPL
	def __init__(self, **kwargs):
		self._filename = kwargs.pop('filename', None)
		self._lineno = kwargs.pop('lineno', None)
		self._text = kwargs.pop('text', None)
		self._offset = kwargs.pop('offset', None)
		super().__init__(**kwargs)

	def __repr__(self):
		msg = super().__repr__()
		return self._tmpl.format(
			filename=self._filename,
			lineno=self._lineno,
			offset=self._offset,
			text=self._text,
			msg=msg
		)
