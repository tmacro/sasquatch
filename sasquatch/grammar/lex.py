import re
from collections import namedtuple
from ..util.fsm import State, Actor
from itertools import chain

VerbT = namedtuple('Verb', ['name'])
NounT = namedtuple('Noun', ['keyword', 'value'])



class Word(State):
	_word_delim = r'.'
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__delim = None
		self._token = ''

	@property
	def _delim(self):
		if self.__delim is None:
			self.__delim = re.compile(self._word_delim)
		return self.__delim

	def _is_end(self, char):
		if char == '':
			return True
		if self._delim.match(char):
			return True
		return False

	def _add(self, char):
		self._token += char


class Verb(Word):
	_valid_previous = [None, 'Noun']
	_valid_next = ['Noun']
	_word_delim = r'[:|]'

	def _process(self, char):
		if char == ' ':
			return None
		if self._is_end(char):
			self._transition('Noun')
			return VerbT(self._token)
		self._add(char)


class Noun(Word):
	_valid_previous = ['Verb', 'Noun']
	_valid_next = ['Verb', 'Noun']
	_word_delim = r'[:|]'
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._keyword = None

	def _process(self, char):
		if char == ' ' and not self._token and not self._keyword:
			return None
		if self._is_end(char):
			if char == ':':
				self._transition('Noun')
			elif char == '|':
				self._transition('Verb')
			return NounT(self._keyword, self._token.rstrip())
		if char == '=' and self._token[:-1] != '\\':
			self._keyword = self._token
			self._token = ''
			return None
		self._add(char)


states = {
	'Verb': Verb,
	'Noun': Noun
}

def _lexer():
	'''Builds a new sq lexer'''
	return Actor('Verb', states)

def tokenize(grammar):
	lexer = _lexer()
	tokens = list(
				filter(
					lambda t: t is not None,
					map(lexer, chain(grammar, ['']))
					)
				)
	return tokens
