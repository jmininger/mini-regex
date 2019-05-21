import unittest as ut
from mini_regex.tokenizer import Token, TokenType, Tokenizer


class TestTokens(ut.TestCase):
    def test_equality(self):
        t1 = Token(TokenType.CHAR, 'a', 0)
        t2 = Token(TokenType.CHAR, 'a', 0)
        t3 = Token(TokenType.CHAR, 'b', 0)
        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)

    def test_type_checks(self):
        t1 = Token(TokenType.CHAR, 'a', 0)
        t2 = Token(TokenType.METACHAR, '.', 0)
        t3 = Token(TokenType.UNION, '|', 0)
        self.assertTrue(t1.is_char())
        self.assertTrue(t2.is_char())
        self.assertTrue(t3.is_union())
        self.assertFalse(t1.is_union())
        self.assertFalse(t3.is_char())
        self.assertEqual(t1.type, TokenType.CHAR)


class TestTokenizer(ut.TestCase):
    # def test_backslash_modifier(self):
    #     t = Tokenizer('a\.')
    #     self.assertEqual(t.next(), Token('a', 'CHAR', (20, 1)))
    #     self.assertEqual(t.next(), Token('.', 'CHAR', (1, 2)))
    #     t2 = Tokenizer('\\\\')
    #     self.assertEqual(t2.next(), Token('\\', 'CHAR', (1, 2)))
    #     self.assertTrue(t2.next().is_end())

    def test_special_tokens(self):
        t = Tokenizer('ab|c((d|.)*)*')
        type_sequence = ['CHAR', 'CHAR', 'UNION', 'CHAR', 'LPAREN', 'LPAREN',
                         'CHAR', 'UNION', 'METACHAR', 'RPAREN', 'STAR',
                         'RPAREN', 'STAR', 'END']

        test_types = [TokenType[t] for t in type_sequence]
        for expected_type in test_types:
            gen_token = t.peek()
            actual_type = gen_token.type
            self.assertEqual(expected_type, actual_type)
            if not gen_token.is_end():
                t.next()

    def test_always_has_end_token(self):
        t = Tokenizer('')
        self.assertEqual(t.peek().type, TokenType.END)
