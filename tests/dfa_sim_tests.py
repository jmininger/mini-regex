from dfa_sim import DFASimulator
from util import table_to_nfa
import unittest as ut


class DFASimTest(ut.TestCase):
    def test_single_char_failure(self):
        # match agains the pattern: 'a'
        table = {0: ({'a': 1}, []), 1: ({}, [])}
        start_state = 0
        end_state = 1
        nfa = table_to_nfa(table, start_state, end_state)
        matcher = DFASimulator(nfa)
        has_match = matcher.advance_state('b')
        self.assertFalse(has_match)

    def test_single_char_match(self):
        table = {0: ({'a': 1}, []), 1: ({}, [])}
        start_state = 0
        end_state = 1
        nfa = table_to_nfa(table, start_state, end_state)
        matcher = DFASimulator(nfa)
        has_match = matcher.advance_state('a')
        self.assertTrue(has_match)
