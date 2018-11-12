from .safe import firstel
from .log import Log

_log = Log('util.fsm')

class Record:
	def __init__(self):
		self._record = []

	def push(self, item):
		self._record.append(item)

	def consume(self, item, number):
		self._record = self._record[:-number]
		self._record.append(item)

	def read(self, number = -1):
		if number == -1:
			return self._record[:]
		return self._record[-number:]

	@property
	def last(self):
		if not self._record:
			return None
		return firstel(self._record[-1:])


class State:
	_valid_previous = []
	_valid_next = []

	def __init__(self, record):
		self._log = Log('util.fsm.State')
		self._record = record
		self._next = False

	@classmethod
	def allow(cls, prev):
		return prev in cls._valid_previous

	def _allow_next(self, state):
		return state in self._valid_next

	def _transition(self, state):
		self._log.debug('Initiating transition to %s'%state)
		if self._allow_next(state):
			self._next = state
			self._log.debug('Successfully initiated transition to %s'%state)
			return True
		self._log.debug('Failed to initiate transition to %s'%state)
		return False

	def __call__(self, data):
		processed = self._process(data)
		if self._next:
			return processed, self._next
		return processed, None

	def _process(self, data):
		# Do processing here
		# Return data to the user or None for nothing
		# call self._transition to change to a new state
		return None


class Actor:
	def __init__(self, starting, states):
		self._log = Log('util.fsm.Actor')
		self._current = None
		self._state = None
		self._possible = states
		self._record = Record()
		self._transition(starting)

	def _transition(self, name):
		state = self._possible.get(name)
		if state is None:
			raise Exception
		self._log.debug('State transition requested to %s'%name)
		if state.allow(self._current):
			self._state = state(self._record)
			self._current = name
			self._log.debug('State transition allowed to %s'%name)
			return True
		self._log.debug('State transition denied to %s'%name)
		return False

	def __call__(self, data):
		data, next_state = self._state(data)
		if next_state is not None:
			self._transition(next_state)
		return data

	@property
	def record(self):
		return self._record.read()
