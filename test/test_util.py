import unittest as ut
import mini_regex.util as util


class NFATableConverterTest(ut.TestCase):
    def test(self):
        # The following table describes the pattern: 'a(b|c)'
        table1 = {
                    0: ({'a': 1}, []),
                    1: ({}, [6]),
                    6: ({}, [2, 4]),
                    4: ({'c': 5}, []),
                    5: ({}, [7]),
                    7: ({}, []),
                    2: ({'b': 3}, []),
                    3: ({}, [7])
                }
        nfa = util.table_to_nfa(table1, 0, 7)
        table2 = util.nfa_to_table(nfa.start)
        self.assertEqual(table1, table2)


class StackTest(ut.TestCase):
    def test_accepts_variable_inputs(self):
        s = util.Stack()
        s.push(*[2, 4, 6])
        actual = []
        for elem in s:
            actual.append(elem)
        self.assertListEqual(actual, [6, 4, 2])

    def test_gets_size(self):
        s = util.Stack()
        s.push(1, 3, 5, 7, 9)
        self.assertEqual(len(s), 5)

    def test_evaluates_to_false_when_empty(self):
        s = util.Stack()
        s.push(5)
        self.assertTrue(s)
        s.pop()
        self.assertFalse(s)

    def test_stack_is_empty(self):
        s = util.Stack()
        self.assertTrue(s.is_empty())
        s.push(1)
        self.assertFalse(s.is_empty())
        s.pop()
        self.assertTrue(s.is_empty())
