
class Action:
	def __init__(self, verb):
		self._verb = verb
		self.__keywords = None

	@property
	def _keywords(self):
		if self.__keywords is None:
			self.__keywords = self._verb.keywords
		return self.__keywords

	def _process(self, value):
		'''
			Is passed a result and is expected to return a result
		'''
		return value


	def __call__(self, results):
		'''
			Expects to be passed a iterable of results
			and to yield a result for each
		'''
		for result in results:
			yield self._process(result)
