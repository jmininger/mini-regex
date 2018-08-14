
import unittest as ut

grammar = {
	'E' : ["T E\'"],
	'E\'': [" | E", ""],
	'T' : ["F T\'"],
	'T\'': [" T ", ""],
	'F' : ["C F\'"],
	'F\'': ["*", ""],
	'C' : [".", "( E )"]
}

class Lexer:
	def __init__(self, regex):
		self._regex = regex
		self._index = 0
	
	def getNext(self):
		while self._regex[self._index] is ' ':
			self._index += 1
		return self.regex[self._index]

class TestLexer(ut.TestCase):
	def test_next_char(self):
		lex = Lexer('ab | cd')
		self.assertEquals(lex.getNext(), 'a')
		self.assertEquals(lex.getNext(), 'b')
		self.assertEquals(lex.getNext(), ' ')
	def test_end_of_stream(self):
		lex = Lexer('ab')
		lex.getNext()
		lex.getNext()
		self.assertEquals(lex.getNext(), None)

if __name__ == '__main__':
    ut.main()
