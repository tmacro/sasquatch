from io import StringIO

class FakeSTDIN(StringIO):
	name = '<stdin>'
