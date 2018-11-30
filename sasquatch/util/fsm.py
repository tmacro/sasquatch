from .conv import firstel
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


class State:
	_name = 'State'
	_valid_previous = []
	_valid_next = []

	def __init__(self, transition):
		self._transition = transition

	@classmethod
	def allow_to(cls, to_state):
		return to_state._name in cls._valid_next

	@classmethod
	def allow_from(cls, from_state):
		if from_state is None:
			return from_state in cls._valid_previous
		return from_state._name in cls._valid_previous

	def __call__(self, data):
		return self._process(data)


class Machine:
	'''FSM for preccessing stream data'''
	def __init__(self, starting, available):
		self._log = Log('util.fsm.Machine')
		self._available = { s._name: s for s in available }
		self._current = None
		self._log.debug('Initilizing Machine, States: %s'%str(self._available))
		self.transition(starting._name)

	def _is_valid(self, name):
		# self._log.debug(type(name))
		return name in self._available

	@staticmethod
	def _invalid_state(name):
		def err(*args, **kwargs):
			raise Exception('%s is not a valid state!'%name._name)
		return err

	def _get_state(self, name):
		self._log.debug(type(name))
		return self._available.get(name, self._invalid_state(name))

	def _needs_transition(self):
		return self._transition_to is not None

	def _do_transition(self):
		if self._needs_transition():
			if self._current and not self._current.allow_to(self._transition_to):
				raise Exception('Cannot transition to %s from %s'%(self._current._name, self._transition_to._name))
			if not self._transition_to.allow_from(self._current):
				raise Exception('Cannot transition from %s to %s'%(self._current._name, self._transition_to._name))
			self._current = self._transition_to(self.transition)
			self._transition_to = None

	def transition(self, new_state):
		self._log.debug('Transitioning to %s'%new_state)
		if self._is_valid(new_state):
			self._transition_to = self._get_state(new_state)

	def process(self, data):
		self._do_transition()
		return self._current(data)

	def __call__(self, data):
		# self._log.debug(data)
		return self.process(data)
