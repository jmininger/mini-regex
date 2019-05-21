from enum import Enum

TokenType = Enum("TokenType",
                 "CHAR LPAREN RPAREN UNION STAR END METACHAR")


class Token:
    """
        A Token is the basic unit of an expression that the parser accepts
    """

    def __init__(self, tok_type, val, pos):
        self.type = tok_type
        self.val = val
        self.pos = pos  # position of the first char in the token

    def __eq__(self, other):
        return self.val == other.val and self.type == other.type

    def __str__(self):
        return (
            "val: "
            + str(self.val)
            + ", type: "
            + str(self.type)
            + ", location"
        )

    def is_char(self):
        return self.type in [TokenType.CHAR, TokenType.METACHAR]

    def is_metachar(self):
        return self.type == TokenType.METACHAR

    def is_star(self):
        return self.type == TokenType.STAR

    def is_union(self):
        return self.type == TokenType.UNION

    def is_lparen(self):
        return self.type == TokenType.LPAREN

    def is_rparen(self):
        return self.type == TokenType.RPAREN

    def is_end(self):
        return self.type == TokenType.END


class Tokenizer:
    """ A token stream """

    special_chars = set(["|", "*", "(", ")", ".", "+"])

    def __init__(self, pattern):
        self.pattern = pattern

        # _stream is a generator object
        self._stream = self._generate_tokens()
        self.next()

    def peek(self):
        return self.peek_char

    def next(self):
        # consider renaming next to advance to make it clear that side effects
        # occur
        self.peek_char = next(self._stream)

    def _generate_tokens(self):
        is_normal_char = False
        for char, pos in zip(self.pattern, range(len(self.pattern))):
            if char in self.special_chars and not is_normal_char:
                tok_type = self._produce_special(char)
                yield Token(tok_type, char, pos)
            elif char == "\\" and not is_normal_char:
                is_normal_char = True
            else:
                # problem here: if escaped char, the size should be two not one
                yield Token(TokenType.CHAR, char, pos)
                if is_normal_char:
                    is_normal_char = False
        yield Token(TokenType.END, "$", len(self.pattern))

    def _produce_special(self, c):
        if c is "|":
            return TokenType.UNION
        if c is "*":
            return TokenType.STAR
        if c is "(":
            return TokenType.LPAREN
        if c is ")":
            return TokenType.RPAREN
        if c is ".":
            return TokenType.METACHAR
