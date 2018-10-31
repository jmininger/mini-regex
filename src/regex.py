import unittest as ut
from parser import RegexParser
from tokenizer import Tokenizer
from dfa_sim import DFASimulator


class MiniRegex:
    def __init__(self, pattern):
        self._pattern = pattern
        self._nfa = self._build_nfa(self._pattern)

    def _build_nfa(self, pattern_str):
        tokenizer = Tokenizer(pattern_str)
        parser = RegexParser(tokenizer)
        return parser.construct_nfa()

    def find_match_atj(self, search_space):
        """ Returns True iff there is a match starting at the first char of the
        search_space argument """
        runner = DFASimulator(self._nfa)
        for c in search_space:
            if runner.advance_state(c):
                return True
            if not runner.is_active():
                return False
        return False

    def is_match(self, search_space):
        """ Returns True iff there is a match starting at the first char of the
        search_space argument """
        runner = DFASimulator(self._nfa)
        for c in search_space:
            if runner.advance_state(c):
                return True
            if not runner.is_active():
                return False
        return False
        # for idx, char in zip(range(len(search_space)), search_space):
        #     for c in search_space[idx+1:]:
        #         if runner.is_active():
        #             match = runner.advance_state(c)
        #             if match:
        #                 return True
        #     runner.reset()
        # return False

    def first_match(self, search_space):
        for i in range(len(search_space)):
            if self.is_match(search_space[i:]):
                return i
        return None


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

    # def test_can_match_patterns_after_first_char(self):
    #     pattern = "hel*o"
    #     regex = MiniRegex(pattern)
    #     search_str = "hi hello"
    #     self.assertEqual(regex.first_match(search_str), 3)

    def test_finds_first_match(self):
        pattern = "hel*o"
        regex = MiniRegex(pattern)
        search_str = "hi hello"
        self.assertTupleEqual((3, 7), regex.first_match(search_str))



if __name__ == '__main__':
    ut.main()

# Should work on files
# Should return the line number and column number of the start of the match
# Record all matches
# Find first match
