import unittest as ut
from mini_regex.tokenizer import Token, Tokenizer


class TestTokens(ut.TestCase):
    def test_equality(self):
        t1 = Token("a", 3)
        t2 = Token("a", 0)
        self.assertEqual(t1, t2)

        t3 = Token("a", 6, True)
        self.assertNotEqual(t1, t3)

    def test_has_val(self):
        t1 = Token("*", 1)
        self.assertTrue(t1.has_val('*'))
        self.assertFalse(t1.has_val('*', True))


class TestTokenizer(ut.TestCase):
    def test_backslash_modifier(self):
        t = Tokenizer('a\\.')
        self.assertEqual(t.peek(), Token('a', None))

        t.advance()
        self.assertEqual(t.peek(), Token('.', None, True))

        t.advance()
        self.assertTrue(t.peek().is_end())

        t2 = Tokenizer('\\\\')
        self.assertEqual(t2.peek(), Token('\\', None, True))
        self.assertTrue(t2.peek().has_val('\\', True))
        t2.advance()
        self.assertTrue(t2.peek().is_end())

    def test_always_has_end_token(self):
        t = Tokenizer('')
        token = t.peek()
        self.assertTrue(token.is_end())
