import re
from collections import namedtuple
from ..util.fsm import State, Machine
from itertools import chain
from ..util.log import Log

_log = Log('grammar.lex')

Context = namedtuple('Context', ['filename', 'lineno', 'offset', 'text'], defaults=[None]*4)
VerbT = namedtuple('Verb', ['name', 'context'], defaults=[None])
NounT = namedtuple('Noun', ['keyword', 'value', 'context'], defaults=[None])

class TextMachine(Machine):
	'''FSM for lexing text into tokens'''
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._offset = None
		self._token_start = None

	def _build_context(self, lineno, token_start, txt, token):
		return  Context(lineno=lineno, offset=token_start, text=txt)

	def _grab_text(self, start, stop, line):
		return line[start:stop]

	def _is_comment(self, line):
		return line.startswith('#')

	def _filter_lines(self, lines):
		for lineno, line in enumerate(lines):
			stripped = line.strip()
			if stripped and not self._is_comment(stripped):
				yield lineno, stripped

	def __call__(self, lines):
		for lineno, line in self._filter_lines(lines):
			token_start = None
			for offset, char in enumerate(chain(line, [''])):
				if token_start is None:
					token_start = offset
				token = self.process(char)
				if token:
					text = self._grab_text(token_start, offset, line)
					ctx = self._build_context(lineno, token_start, text, token)
					yield token._replace(context=ctx)
					token_start = None

class FileMachine(TextMachine):
	def _build_context(self, *args, **kwargs):
		ctx = super()._build_context(*args, **kwargs)
		return ctx._replace(filename=self._filename)


	def __call__(self, fd):
		self._filename = fd.name
		return super().__call__(fd.readlines())

class Word(State):
	_name: 'Word'
	_word_delim = r'.'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__delim = None
		self._token = ''
		self._text = ''

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

	_ws_regex = re.compile(r'\w')
	def _is_ws(self, char):
		if self._ws_regex.match(char):
			return True
		return False

	def _add(self, char):
		self._token += char


class Verb(Word):
	_name = 'Verb'
	_valid_previous = [None, 'Noun', 'Verb']
	_valid_next = ['Noun', 'Verb']
	_word_delim = r'[:|#]'

	def _process(self, char):
		if char == ' ':
			return None
		if self._is_end(char):
			if char == ':':
				self._transition('Noun')
			elif char == '|':
				self._transition('Verb')
			return VerbT(self._token)
		self._add(char)


class Noun(Word):
	_name = 'Noun'
	_valid_previous = ['Verb', 'Noun']
	_valid_next = ['Verb', 'Noun']
	_word_delim = r'[:|\n#]'

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

states = [
	Verb,
	Noun,
]

def _lexer():
	'''Builds a new sq lexer'''
	_log.debug('Building Lexer')
	return FileMachine(Verb, states)

def tokenize(grammar):
	_log.debug('Lexing %s'%grammar)
	lexer = _lexer()
	tokens = list(
				filter(
					lambda t: t is not None,
					lexer(grammar)
					)
				)
	_log.debug('Lexed lines to %s'%tokens)
	return tokens
