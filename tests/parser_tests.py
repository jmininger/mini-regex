import parser
from util import nfa_to_table, table_to_nfa
from nfa import NFAState
import unittest as ut


class ParserTest(ut.TestCase):
    def test_concat_adds_single_epsilon(self):
        expected = {
                0: ({'a': 1}, []),
                1: ({}, [2]),
                2: ({'b': 3}, []),
                3: ({}, [])}
        a_nfa = table_to_nfa({0: ({'a': 1}, []), 1: ({}, [])}, 0, 1)
        b_nfa = table_to_nfa({2: ({'b': 3}, []), 3: ({}, [])}, 2, 3)
        concat_graph = parser.concat(a_nfa, b_nfa)
        actual = nfa_to_table(concat_graph)
        self.assertSetEqual(set(expected.keys()), set(actual.keys()))
