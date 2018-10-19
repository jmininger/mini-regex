from enum import Enum


TokenType = Enum('TokenType',
                 '''CHAR,
                 LPAREN,
                 RPAREN,
                 UNION,
                 STAR,
                 END,
                 METACHAR''')


class Token:
    """
        Represents the basic unit of an expression that the parser accepts
    """
    def __init__(self, tok_type, val):
        self.type = tok_type
        self.val = val

    def __eq__(self, other):
        return self.val == other.val and self.type == other.type

    def __str__(self):
        return "val: " + str(self.val) + ", type: " + str(self.type) \
                + ", location"

    def is_char_type(self):
        return self.type in [TokenType.CHAR, TokenType.METACHAR]

    def is_operator_type(self):
        return self.type in [TokenType.UNION, TokenType.STAR]

    def is_end_type(self):
        return self.type == TokenType.END


class Tokenizer:
    special_chars = set(['|', '*', '(', ')', '.', '+'])

    def __init__(self, pattern):
        self.pattern = pattern

        # _stream is a generator object
        self._stream = self._generate_tokens()

    def next(self):
        return next(self._stream)

    def _generate_tokens(self):
        is_normal_char = False
        for char in self.pattern:
            if char in self.special_chars and not is_normal_char:
                tok_type = self._produce_special(char)
                yield Token(tok_type, char)
            elif char == '\\' and not is_normal_char:
                is_normal_char = True
            else:
                # problem here: if escaped char, the size should be two not one
                yield Token(TokenType.CHAR, char)
                if is_normal_char:
                    is_normal_char = False
        yield Token(TokenType.END, '$')

    def _produce_special(self, c):
        if c is '|':
            return TokenType.OR
        if c is '*':
            return TokenType.STAR
        if c is '(':
            return TokenType.LPAREN
        if c is ')':
            return TokenType.RPAREN
        if c is '.':
            return TokenType.METACHAR
