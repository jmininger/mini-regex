from mini_regex.dfa_sim import DFASimulator
from mini_regex.util import table_to_nfa
import unittest as ut


class DFASimTest(ut.TestCase):
    def test_single_char_failure(self):
        # match agains the pattern: 'a'
        table = {0: [("char: a", 1)],
                 1: []}
        start_state = 0
        end_state = 1
        nfa = table_to_nfa(table, start_state, end_state)
        runner = DFASimulator(nfa)
        runner.advance_state('b')
        match = runner.check_match()
        self.assertIsNone(match)

    def test_single_char_match(self):
        table = {0: [("char: a", 1)],
                 1: []}
        start_state = 0
        end_state = 1
        nfa = table_to_nfa(table, start_state, end_state)
        runner = DFASimulator(nfa)
        runner.advance_state('a')

        match_end = runner.check_match()
        self.assertEqual(match_end, 1)

# NOTE: This test case is no longer relevant since greediness is now controlled
# by the MiniRegex class
#     def test_greedy_matches(self):
#         # Represents "ab|a"
#         table = {0: [("char: a", 1)],
#                  1: [("char: b", 2)],
#                  2: [("epsilon", 6)],
#                  3: [("char: a", 4)],
#                  4: [("epsilon", 6)],
#                  5: [("epsilon", 0), ("epsilon", 3)],
#                  6: []}
#         nfa = table_to_nfa(table, 5, 6)
#         runner = DFASimulator(nfa)
#         self.assertTupleEqual((0, 0), runner.advance_multi_state('a'))
#         self.assertTupleEqual((0, 1), runner.advance_multi_state('b'))

    def test_overlap_doesnt_affect_dfa_sim(self):
        # Table for:  'abc|bcde'
        table = {14: [("epsilon", 0), ("epsilon", 6)],
                 6: [("char: b", 7)],
                 7: [("char: c", 9)],
                 9: [("char: d", 11)],
                 11: [("char: e", 13)],
                 13: [("epsilon", 15)],
                 15: [],
                 0: [("char: a", 1)],
                 1: [("char: b", 3)],
                 3: [("char: c", 5)],
                 5: [("epsilon", 15)]}
        nfa = table_to_nfa(table, 14, 15)
        runner = DFASimulator(nfa)
        runner.advance_state('a')
        match_end = runner.check_match()
        self.assertIsNone(match_end)

        self.assertListEqual([iter.node.id for iter in
                             runner.dfa.get_substates()], [1])

        runner.advance_state('b')
        runner.advance_state('c')
        match_end = runner.check_match()
        self.assertEqual(match_end, 3)

        runner.advance_state('d')
        match_end = runner.check_match()
        self.assertIsNone(match_end)
