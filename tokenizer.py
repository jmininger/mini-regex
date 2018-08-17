import unittest as ut


class Token:
    """
        Represents the basic unit of an expression that the parser accepts
    """
    tok_types = ['CHAR', 'LPAREN', 'RPAREN', 'OR', 'STAR', 'END', 'METACHAR']

    def __init__(self, val, tok_type, loc):
        self._val = val
        self._loc = loc
        if tok_type in self.tok_types:
            self._tok_type = tok_type
        else:
            pass
        # TODO Figure out how to throw exception here

    @property
    def tok_type(self):
        return self._tok_type

    def __eq__(self, other):
        return self._val == other._val and self._tok_type == other._tok_type

    def __str__(self):
        return "val: " + str(self._val) + ", type: " + str(self._tok_type) \
                + ", location, len: " + str(self._loc)

    def is_char_type(self):
        return self._tok_type in ['CHAR', 'METACHAR']

    def is_operator_type(self):
        return self._tok_type in ['OR', 'STAR']

    def is_end_type(self):
        return self._tok_type == 'END'


class TestTokens(ut.TestCase):
    def test_equality(self):
        t1 = Token('a', 'CHAR', 1)
        t2 = Token('a', 'CHAR', 2)
        t3 = Token('b', 'CHAR', 3)
        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)

    def test_type_checks(self):
        t1 = Token('a', 'CHAR', 1)
        t2 = Token('.', 'METACHAR', 2)
        t3 = Token('|', 'OR', 3)
        self.assertTrue(t1.is_char_type())
        self.assertTrue(t2.is_char_type())
        self.assertTrue(t3.is_operator_type())
        self.assertFalse(t1.is_operator_type())
        self.assertFalse(t3.is_char_type())
        self.assertEqual(t1.tok_type, 'CHAR')


class Tokenizer:
    special_chars = set(['|', '*', '(', ')', '.'])

    def __init__(self, pattern):
        self._pattern = pattern
        # _stream is a generator object
        self._stream = self._generate_tokens()
        self._position = 0

    def next(self):
        return next(self._stream)

    def _generate_tokens(self):
        isNormalChar = False
        for i, c in enumerate(self._pattern):
            if c in self.special_chars and not isNormalChar:
                tok_type = self._produce_special(c)
                yield Token(c, tok_type, (i, 1))
            elif c == '\\' and not isNormalChar:
                isNormalChar = True
            else:
                # problem here: if escaped char, the size should be two not one
                yield Token(c, 'CHAR', (i, 1))
                if isNormalChar:
                    isNormalChar = False
        yield Token('$', 'END', (len(self._pattern), 1))

    def _produce_special(self, c):
        if c is '|':
            return 'OR'
        if c is '*':
            return 'STAR'
        if c is '(':
            return 'LPAREN'
        if c is ')':
            return 'RPAREN'
        if c is '.':
            return 'METACHAR'


class TestTokenizer(ut.TestCase):
    def test_backslash_modifier(self):
        t = Tokenizer('a\.')
        self.assertEqual(t.next(), Token('a', 'CHAR', (20, 1)))
        self.assertEqual(t.next(), Token('.', 'CHAR', (1, 2)))
        t2 = Tokenizer('\\\\')
        self.assertEqual(t2.next(), Token('\\', 'CHAR', (1, 2)))
        self.assertTrue(t2.next().is_end_type())

    def test_special_tokens(self):
        t = Tokenizer('ab|c((d|.)*)*')
        test_types = [
                'CHAR', 'CHAR', 'OR', 'CHAR', 'LPAREN', 'LPAREN', 'CHAR',
                'OR', 'METACHAR', 'RPAREN', 'STAR', 'RPAREN', 'STAR', 'END']
        for expected_type in test_types:
            actual_type = t.next()._tok_type
            self.assertEqual(expected_type, actual_type)


if __name__ == '__main__':
    ut.main()
