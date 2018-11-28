from enum import Enum
from functools import partial

class RecordType(Enum):
	SINGLE = 1
	LIST = 2

class DataTypes(Enum):
	BUCKET = 1
	OBJECT = 2

def _extract_record(key, data):
	for value in data.get(key, [])
		yield value

def extract_record(name):
	def outer(f):
		def inner(*args, **kwargs):
			return partial(_extract_record, name), f(*args, **kwargs)
		return inner
	return outer
