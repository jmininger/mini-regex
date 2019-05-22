class Token:
    """
        A Token is the basic unit of an expression that the parser uses.
    """

    def __init__(self, val, pos, escaped=False, end=False):
        self.val = val
        self.pos = pos  # position of the first char in the token
        self.escaped = escaped
        self._is_end = end

    def __eq__(self, other):
        return self.val == other.val and self.escaped == other.escaped

    def __str__(self):
        return (
            "esc: " + str(self.escaped) +
            ", val: " + str(self.val) +
            ", location: " + str(self.pos)
        )

    def __repr__(self):
        return str(self.val) + " " + str(self.escaped) + " " + str(self.pos)

    def has_val(self, char, escaped=False):
        return self.val == char and self.escaped == escaped

    def is_end(self):
        return self._is_end


class Tokenizer:
    """ A token stream """

    def __init__(self, pattern):
        self.pattern = pattern
        # _stream is a generator object
        self._stream = self._generate_tokens()
        self.peek_char = None
        # sets 'self.peek_char'
        self.advance()

    def peek(self):
        return self.peek_char

    def advance(self):
        """ 'Eats' a token in the stream; no return value """
        self.peek_char = next(self._stream)

    def _generate_tokens(self):
        pattern = self.pattern
        pattern_len = len(pattern)

        escaped_flag = False
        for char, pos in zip(pattern, range(pattern_len)):
            if escaped_flag:
                token = Token(char, pos-1, True)
                escaped_flag = False
                yield token
            elif char is "\\":
                escaped_flag = True
            else:
                token = Token(char, pos)
                yield token

        # Stream is empty, return the EOF token
        yield Token("", -1, False, True)
