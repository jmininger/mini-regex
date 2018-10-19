import unittest as ut
from tokenizer import Token, TokenType, Tokenizer


class TestTokens(ut.TestCase):
    def test_equality(self):
        t1 = Token(TokenType.CHAR, 'a')
        t2 = Token(TokenType.CHAR, 'a')
        t3 = Token(TokenType.CHAR, 'b')
        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)

    def test_type_checks(self):
        t1 = Token(TokenType.CHAR, 'a')
        t2 = Token(TokenType.METACHAR, '.')
        t3 = Token(TokenType.UNION, '|')
        self.assertTrue(t1.is_char_type())
        self.assertTrue(t2.is_char_type())
        self.assertTrue(t3.is_operator_type())
        self.assertFalse(t1.is_operator_type())
        self.assertFalse(t3.is_char_type())
        self.assertEqual(t1.type, TokenType.CHAR)


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
        type_sequence = ['CHAR', 'CHAR', 'OR', 'CHAR', 'LPAREN', 'LPAREN',
                         'CHAR', 'OR', 'METACHAR', 'RPAREN', 'STAR', 'RPAREN',
                         'STAR', 'END']

        test_types = [TokenType[t] for t in type_sequence]
        for expected_type in test_types:
            gen_token = t.next()
            actual_type = gen_token.type
            self.assertEqual(expected_type, actual_type)
