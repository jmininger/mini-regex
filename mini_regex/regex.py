import unittest as ut
from mini_regex.parser import RegexParser
from mini_regex.tokenizer import Tokenizer
from mini_regex.dfa_sim import DFASimulator


class MiniRegex:
    def __init__(self, pattern):
        self._pattern = pattern
        self._nfa = self._build_nfa(self._pattern)

    def _build_nfa(self, pattern_str):
        tokenizer = Tokenizer(pattern_str)
        parser = RegexParser(tokenizer)
        return parser.construct_nfa()

    def find_match_at(self, search_space):
        """ Returns True iff there is a match starting at the first char of the
        search_space argument """
        runner = DFASimulator(self._nfa)
        for c in search_space:
            if runner.advance_multi_state(c):
                return True
            if not runner.is_active():
                return False
        return False

    def find_all_matches(self, search_space):
        runner = DFASimulator(self._nfa)
        matches = {}  # start_index: end_index
        for c in search_space:
            match = runner.advance_multi_state(c)
            if match:
                start_idx, end_idx = match
                matches[start_idx] = end_idx
        return [(start, end) for start, end in matches.items()]

    # def is_match(self, search_space):
    #     search_space argument """
    #     runner = DFASimulator(self._nfa)
    #     for c in search_space:
    #         if runner.advance_state(c):
    #             return True
    #         if not runner.is_active():
    #             return False
    #     return False

    def first_match(self, search_space):
        for i in range(len(search_space)):
            if self.is_match(search_space[i:]):
                return i
        return None


# Everything should be feature first, and not worry about the implementation.
# As long as it works, its ok.
class TestRegexEngine(ut.TestCase):
    def test_single_char_match(self):
        pattern = "a"
        regex = MiniRegex(pattern)
        search_str = "a"
        self.assertListEqual(regex.find_all_matches(search_str), [(0, 0)])

    def test_single_match(self):
        pattern = ".el*o"
        regex = MiniRegex(pattern)

        search_str = "Hello World!"
        self.assertListEqual(regex.find_all_matches(search_str), [(0, 4)])

        search_str = "Yelllloooooooee"
        self.assertListEqual(regex.find_all_matches(search_str), [(0, 6)])

        search_str = "Not a match"
        self.assertListEqual(regex.find_all_matches(search_str), [])

    def test_is_greedy(self):
        pattern = "a|ab"
        regex = MiniRegex(pattern)
        search_str = "ab"
        self.assertListEqual([(0, 1)], regex.find_all_matches(search_str))

    def test_overlapping_matches(self):
        pattern = "abc|bcde"
        regex = MiniRegex(pattern)
        search_str = "abcde"
        self.assertListEqual(regex.find_all_matches(search_str), [(0, 2)])

    def test_matches_occuring_later(self):
        pattern = "abc|bcde"
        regex = MiniRegex(pattern)
        search_str = "kbcde"
        self.assertListEqual(regex.find_all_matches(search_str), [(1, 4)])


if __name__ == "__main__":
    ut.main()

# Should work on files
# Should return the line number and column number of the start of the match
# Record all matches
# Find first match
