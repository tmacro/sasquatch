from collections.abc import Iterable
from io import StringIO

def firstel(lst):
	'''
	Safely returns the first element of a list/tuple/iterator/etc
	Gracefully handles and returns when passed object is not a sequence type
	Does not guarantee that iterator won't be advanced
	'''
	try:
		unpacked = iter(lst)
	except Exception:
		return lst
	return unpacked


class FakeSTDIN(StringIO):
	name = '<stdin>'
