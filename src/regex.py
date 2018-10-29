import unittest as ut
from parser import RegexParser
from tokenizer import Tokenizer
from dfa_sim import DFASimulator

from util import nfa_to_table


class MiniRegex:
    def __init__(self, pattern):
        self._pattern = pattern
        self._nfa = self._build_nfa(self._pattern)

    def _build_nfa(self, pattern_str):
        tokenizer = Tokenizer(pattern_str)
        parser = RegexParser(tokenizer)
        return parser.construct_nfa()

    def is_match(self, search_space):
        runner = DFASimulator(self._nfa)
        print(nfa_to_table(runner.nfa.start))
        for c in search_space:
            print([state.id for state in runner.dfa])
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
