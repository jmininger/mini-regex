from nfa import State, NFA
from transitions import Transition
import unittest as ut


class TransitionStub(Transition):
    def __init__(self, available_set, is_epsilon=False):
        self.available_set = available_set
        self.is_epsilon = is_epsilon

    def is_available(self, char):
        if self.is_epsilon:
            return True
        else:
            return char in self.available_set


class StateTest(ut.TestCase):
    def test_returns_only_matching_transitions(self):
        state = State(0)
        avail_trans = TransitionStub(set(['a']))
        unavail_trans = TransitionStub(set())
        state.add_path(avail_trans, 1)
        state.add_path(unavail_trans, 2)
        paths = state.available_paths('a')
        self.assertEquals(1, len(paths))
        self.assertListEqual([1], paths)

    def test_returns_only_epsilon_transitions_on_empty_str(self):
        state = State(0)
        epsilon = TransitionStub(set(), True)
        normal_transition = TransitionStub(set(['a']))
        state.add_path(epsilon, 1)
        state.add_path(epsilon, 2)
        state.add_path(normal_transition, 3)
        result = state.available_paths('')
        self.assertListEqual(result, [1, 2])


class StateStub(State):
    def __init__(self, id, table):
        self.id = id
        self.table = table

    def available_paths(self, char):
        epsilons = self.table[''] if '' in self.table else []
        if char in self.table:
            return set((self.table[char]) + epsilons)
        else:
            return set(epsilons)


class NFATest(ut.TestCase):
    min_trans_table = {
            0: StateStub(0, {'': [1]}),
            1: StateStub(1, {})
            }

    def test_start_state_is_valid_state(self):
        self.assertRaisesRegex(
                Exception,
                'start state is not a valid state',
                NFA, self.min_trans_table, 2, [1]
                )

    def test_end_states_are_valid(self):
        self.assertRaisesRegex(
                Exception,
                'end states are not all valid states',
                NFA, self.min_trans_table, 0, [1, 2]
                )

    def test_calculates_epsilon_closure(self):
        trans_table = {
                0: StateStub(0, {'': [1, 2]}),
                1: StateStub(1, {'a': [5], '': [4]}),
                2: StateStub(2, {'': [3]}),
                3: StateStub(3, {'': [1]}),
                4: StateStub(4, {}),
                5: StateStub(5, {'': [6]}),
                6: StateStub(6, {'': [0, 5]})
                }
        nfa = NFA(trans_table, 0, [4])
        # Makes sure that a closure does not include itself
        epsilon_closure0 = nfa.epsilon_closure(0)
        self.assertSetEqual(epsilon_closure0, set([1, 2, 3, 4]))

        epsilon_closure4 = nfa.epsilon_closure(4)
        self.assertSetEqual(epsilon_closure4, set([]))

        # This instance ensures that the closure includes the origin state if
        # there is a cycle in the graph
        epsilon_closure5 = nfa.epsilon_closure(5)
        self.assertSetEqual(epsilon_closure5, set([0, 1, 2, 3, 4, 5, 6]))
