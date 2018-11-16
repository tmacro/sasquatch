












class DataView:
	def __init__(self):
		self.__mapping = {}
		self.__data = None

	def _map_key(self, key):
		return self.__mapping.get(key)

	def __getattr__(self, key):
		val = self.__mapping.get(key)
		if val is not None:
			return val
		raise AttributeError

	def _register(self, key, val, overwrite = False):
		if key in self.__hooks and not overwrite:
			raise Exception('Hook already registered %s'%key)
		self.__hooks[key] = val
