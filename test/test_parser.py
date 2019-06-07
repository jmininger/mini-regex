import mini_regex.parser as parser
from mini_regex.tokenizer import Tokenizer
from mini_regex.util import nfa_to_table, table_to_nfa
# from mini_regex.nfa import NFAState
import unittest as ut


class ParserTest(ut.TestCase):
    def test_concat_merges_two_states_to_one(self):
        a_table = {0: [("char: a", 1)], 1: []}
        a_nfa = table_to_nfa(a_table, 0, 1)
        b_table = {2: [("char: b", 3)], 3: []}
        b_nfa = table_to_nfa(b_table, 2, 3)
        concat_graph = parser.concat(a_nfa, b_nfa)
        actual_table = nfa_to_table(concat_graph.start)
        expected_states = len(a_table.keys()) + len(b_table.keys()) - 1
        self.assertEqual(len(actual_table.keys()), expected_states)

    def test_concat_adds_single_epsilon(self):
        # state 2 is removed by concat, when it is merged with state 1
        expected = {
                0: [("char: a", 1)],
                1: [("char: b", 3)],
                3: []}
        a_nfa = table_to_nfa({0: [("char: a", 1)], 1: []}, 0, 1)
        b_nfa = table_to_nfa({2: [("char: b", 3)], 3: []}, 2, 3)

        concat_graph = parser.concat(a_nfa, b_nfa)
        actual = nfa_to_table(concat_graph.start)
        self.assertEqual(expected, actual)

    def test_union_adds_2_states(self):
        expected = {
                0: [("char: a", 1)],
                1: [("epsilon", 5)],
                2: [("char: b", 3)],
                3: [("epsilon", 5)],
                4: [("epsilon", 0), ("epsilon", 2)],
                5: []}
        a_nfa = table_to_nfa({0: [("char: a", 1)], 1: []}, 0, 1)
        b_nfa = table_to_nfa({2: [("char: b", 3)], 3: []}, 2, 3)
        id_alloc = CounterStub(4)
        result_nfa = parser.union(a_nfa, b_nfa, id_alloc)
        result = nfa_to_table(result_nfa.start)
        self.assertEqual(expected, result)

    def test_kstar(self):
        # represents : "a"
        nfa = table_to_nfa({0: [("char: a", 1)], 1: []}, 0, 1)
        expected = {0: [("char: a", 1)],
                    1: [("epsilon", 0), ("epsilon", 3)],
                    2: [("epsilon", 0), ("epsilon", 3)],
                    3: []}
        id_alloc = CounterStub(2)
        result_nfa = parser.kstar(nfa, id_alloc)
        actual = nfa_to_table(result_nfa.start)
        self.assertEqual(expected, actual)

    # def test_elem_plus_equal_to_elem_elem_kstar(self):
    #     """ (a+) is equivalent to (aa*)
    #     """
    #     expected = {0: [("char: a", 1)],
    #                 1: [("epsilon", 0), ("epsilon", 3)],
    #                 3: []}

    #     # represents = "a"
    #     nfa = table_to_nfa({0: [("char: a", 1)], 1: []}, 0, 1)
    #     id_alloc = CounterStub(2)
    #     result_nfa = parser.repeater(nfa, '+', id_alloc)
    #     actual = nfa_to_table(result_nfa.start)
    #     print(actual)
    #     self.assertEqual(expected, actual)

    def test_parenthesis_builds_inner_nfa_first(self):
        # Note the difference between "(ab)*" and ab*
        re_parser1 = parser.RegexParser(Tokenizer("(ab)*"))
        nfa1 = re_parser1.construct_nfa()
        table1 = nfa_to_table(nfa1.start)

        re_parser2 = parser.RegexParser(Tokenizer("ab*"))
        nfa2 = re_parser2.construct_nfa()
        table2 = nfa_to_table(nfa2.start)
        self.assertNotEqual(table1, table2)

    def test_basic_parse(self):
        re_parser1 = parser.RegexParser(Tokenizer("[^1-3a]"))
        nfa1 = re_parser1.construct_nfa()
        table1 = nfa_to_table(nfa1.start)
        expected = {0: [("neg-class: 1-3a", 1)],
                    1: []}
        self.assertEqual(table1, expected)


class CounterStub:
    def __init__(self, start_val):
        self.val = start_val

    def create_id(self):
        val = self.val
        self.val += 1
        return val
