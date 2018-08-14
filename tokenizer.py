import unittest as ut


class Token:
    tok_types = ['CHAR', 'LPAREN', 'RPAREN', 'OR', 'STAR', 'END', 'METACHAR']

    def __init__(self, val, tok_type, loc):
        self._val = val
        self._loc = loc
        if tok_type in self.tok_types:
            self._tok_type = tok_type
        else:
            pass
        # TODO Figure out how to throw exception here

    def __str__(self):
        return str(self._val, self._tok_type)

    def __eq__(self, other):
        return self._val == other._val and self._tok_type == other._tok_type

    def isCharType(self):
        return self._tok_type in ['CHAR', 'METACHAR']

    def isOperatorType(self):
        return self._tok_type in ['OR', 'STAR']


class TestTokens(ut.TestCase):
    def testEquality(self):
        t1 = Token('a', 'CHAR', 1)
        t2 = Token('a', 'CHAR', 2)
        t3 = Token('b', 'CHAR', 3)
        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)

    def testTypeChecks(self):
        t1 = Token('a', 'CHAR', 1)
        t2 = Token('.', 'METACHAR', 2)
        t3 = Token('|', 'OR', 3)
        self.assertTrue(t1.isCharType())
        self.assertTrue(t2.isCharType())
        self.assertTrue(t3.isOperatorType())
        self.assertFalse(t1.isOperatorType())
        self.assertFalse(t3.isCharType())


class Tokenizer:

    def __init__(self, pattern):
        self._pattern = pattern
        # _stream is a generator object
        self._stream = self._getToken()
        # keep track of num_chars consumed and the len of each tok

    def next(self):
        return next(self._stream)

    def _getToken(self):
        isNormalChar = False
        for c in self._pattern:
            if c in ['|', '*', '(', ')', '.'] and not isNormalChar:
                yield self._produceSpecial(c)
            elif c == '\\':
                isNormalChar = True
            else:
                yield Token(c, 'CHAR')
                isNormalChar = False
            yield Token('$', 'END')

    def _produceSpecial(c):
        if c is '|':
            return Token(c, 'OR')
        if c is '*':
            return Token(c, 'STAR')
        if c is '(':
            return Token(c, 'LPAREN')
        if c is ')':
            return Token(c, 'RPAREN')
        if c is '.':
            return Token(c, 'ALLCHAR')


'''
We want to take a string as input, store it as a stream?? We want
Every automata has a match() func that determines the next transition
'''


class TestTokenizer(ut.TestCase):
    def testLexCharactersTest(self):
        t = Tokenizer('ab')
        if t.next() == Token('a', 'CHAR'):
            self.assertEquals(5, 5)
        else:
            self.assertEquals(t.next(), 0)


if __name__ == '__main__':
    ut.main()
