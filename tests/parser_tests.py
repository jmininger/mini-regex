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
        actual = nfa_to_table(concat_graph[0])
        self.assertSetEqual(set(expected.keys()), set(actual.keys()))
        for state_id in actual.keys():
            self.assertTupleEqual(actual[state_id], expected[state_id])

    def test_union_adds_2_states(self):
        expected = {
                0: ({'a': 1}, []),
                1: ({}, [5]),
                2: ({'b': 3}, []),
                3: ({}, [5]),
                4: ({}, [0, 2]),
                5: ({}, [])}
        a_nfa = table_to_nfa({0: ({'a': 1}, []), 1: ({}, [])}, 0, 1)
        b_nfa = table_to_nfa({2: ({'b': 3}, []), 3: ({}, [])}, 2, 3)
        id_alloc = CounterStub(4)
        result_nfa = parser.union(a_nfa, b_nfa, id_alloc)
        result = nfa_to_table(result_nfa[0])
        self.assertEqual(expected, result)


class CounterStub:
    def __init__(self, start_val):
        self.val = start_val

    def create_id(self):
        val = self.val
        self.val += 1
        return val
