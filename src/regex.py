import unittest as ut


class MiniRegex:
    def __init__(self, pattern):
        self._pattern = pattern
        self._nfa = self._build_nfa(self._pattern)

    def _build_nfa(self, pattern_str):
        pass

    def is_match(self, search_space):
        return self._pattern in search_space


# Everything should be feature first, and not worry about the implementation.
# As long as it works, its ok.
class TestRegexEngine(ut.TestCase):

    def test_single_match(self):
        pattern = '.el*o'
        regex = MiniRegex(pattern)
        search_str = 'Hello World!'
        self.assertTrue(regex.is_match(search_str))

        search_str = 'Telllloooooooee'
        self.assertTrue(regex.is_match(search_str))

        search_str = 'Not a match'
        self.assertFalse(regex.is_match(search_str))

    def test_reuse_pattern(self):
        pass

    def test_first_match(self):
        pass

    def test_longer_match(self):  # scenario where regex gets chopped off but
        # states remain
        pass


if __name__ == '__main__':
    ut.main()

# Should work on files
# Should return the line number and column number of the start of the match
# Record all matches
# Find first match
