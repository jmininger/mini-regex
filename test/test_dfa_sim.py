from mini_regex.dfa_sim import DFASimulator
from mini_regex.util import table_to_nfa
import unittest as ut


class DFASimTest(ut.TestCase):
    def test_single_char_failure(self):
        # match agains the pattern: 'a'
        table = {0: ({'a': 1}, []), 1: ({}, [])}
        start_state = 0
        end_state = 1
        nfa = table_to_nfa(table, start_state, end_state)
        matcher = DFASimulator(nfa)
        has_match = matcher.advance_multi_state('b')
        self.assertFalse(has_match)

    def test_single_char_match(self):
        table = {0: ({'a': 1}, []), 1: ({}, [])}
        start_state = 0
        end_state = 1
        nfa = table_to_nfa(table, start_state, end_state)
        matcher = DFASimulator(nfa)
        has_match = matcher.advance_multi_state('a')
        self.assertTrue(has_match)

    def test_greedy_matches(self):
        # Represents "ab|a"
        table = {
                0: ({"a": 1}, []),
                1: ({'b': 2}, []),
                2: ({}, [6]),
                3: ({'a': 4}, []),
                4: ({}, [6]),
                5: ({}, [0, 3]),
                6: ({}, [])
                }
        nfa = table_to_nfa(table, 5, 6)
        matcher = DFASimulator(nfa)
        self.assertTupleEqual((0, 0), matcher.advance_multi_state('a'))
        self.assertTupleEqual((0, 1), matcher.advance_multi_state('b'))

    def test_(self):
        # 'abc|bcde'
        table = {14: ({}, [0, 6]), 6: ({'b': 7}, []), 7: ({'c': 9}, []),
                 9: ({'d': 11}, []), 11: ({'e': 13}, []), 13: ({}, [15]),
                 15: ({}, []), 0: ({'a': 1}, []), 1: ({'b': 3}, []),
                 3: ({'c': 5}, []), 5: ({}, [15])}
        nfa = table_to_nfa(table, 14, 15)
        matcher = DFASimulator(nfa)
        match = matcher.advance_multi_state('a')
        self.assertIsNone(match)
        self.assertListEqual([iter.substate.id for iter in
                             matcher.dfa.get_iterators()], [1])
