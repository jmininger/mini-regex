from mini_regex.parser import RegexParser
from mini_regex.tokenizer import Tokenizer
from mini_regex.dfa_sim import DFASimulator  # , MultiDFASimulator
from mini_regex.match import Match, remove_overlaps


class MiniRegex:
    def __init__(self, pattern, greedy=True):
        self._pattern = pattern
        self._nfa = self._build_nfa(self._pattern)

        self._greedy = greedy

    def _build_nfa(self, pattern_str):
        tokenizer = Tokenizer(pattern_str)
        parser = RegexParser(tokenizer)
        return parser.construct_nfa()

    def find_match_at(self, search_space, start_idx=0):
        """ Returns match object
        """
        runner = DFASimulator(self._nfa)
        result = Match()
        match = runner.check_match()

        # the following checks must be done before the main loop in case the
        # dfa has completed before any chars have been fed in.
        # An example would be the pattern:
        #   'a*' (with greedy set to false )
        #   The above regex will be a match before any
        #   characters from the search_string are fed in.

        # only return early if not greedy
        if match and not self._greedy:
            return Match(search_space, 0, match, start_idx)
        elif match:
            result = Match(search_space, 0, match, start_idx)
        if runner.check_finished():
            return result

        # main loop
        for c in search_space:
            runner.advance_state(c)
            match = runner.check_match()
            if match and not self._greedy:
                return Match(search_space, 0, match, start_idx)
            elif match:
                result = Match(search_space, 0, match, start_idx)
            if runner.check_finished():
                break
        # no more chars to feed runner; search over
        return result

    def find_all_matches(self, search_str):
        result = []
        for i in range(len(search_str)):
            match = self.find_match_at(search_str[i:], i)
            if match.has_value():
                result.append(match)
        return remove_overlaps(result)

    def first_match(self, search_space):
        for i in range(len(search_space)):
            match = self.find_match_at(search_space[i:], i)
            if(match.has_value()):
                return match
        return Match()

    # def is_match(self, search_space):
    #     match = self.find_match_at(search_space)
    #     if match.has_value():
    #         return True
    #     else:
    #         return False

    # def find_all_matches(self, search_space):
    #     runner = MultiDFASimulator(self._nfa)
    #     matches = {}  # start_index: end_index
    #     for c in search_space:
    #         match = runner.advance_multi_state(c)
    #         if match:
    #             start_idx, end_idx = match
    #             matches[start_idx] = end_idx
    #     return [(start, end) for start, end in matches.items()]
