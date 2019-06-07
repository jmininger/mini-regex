from mini_regex.nfa import NFAState
from mini_regex.transitions import Transition
import unittest as ut


class TransitionStub(Transition):
    def __init__(self, available_set, desc, is_epsilon=False):
        self.available_set = available_set
        self.is_epsilon = is_epsilon
        self._desc = desc

    def is_available(self, char):
        if self.is_epsilon:
            return True
        else:
            return char in self.available_set

    def eats_input(self):
        return not self.is_epsilon


class NFAStateTest(ut.TestCase):
    def test_returns_only_matching_transitions(self):
        state = NFAState(0)
        avail_trans = TransitionStub(set(['a']), "char: a")
        unavail_trans = TransitionStub(set(), "")
        state.add_path(avail_trans, 1)
        state.add_path(unavail_trans, 2)
        paths = state.available_cost_paths('a')
        self.assertEqual(1, len(paths))
        self.assertSetEqual(set([1]), paths)

    def test_returns_only_epsilon_transitions_on_empty_str(self):
        state = NFAState(0)
        epsilon = TransitionStub(set(), "epsilon", True)
        normal_transition = TransitionStub(set(['a']), "char: a")
        state.add_path(epsilon, 1)
        state.add_path(epsilon, 2)
        state.add_path(normal_transition, 3)
        result = state.available_cost_paths('')
        self.assertSetEqual(result, set())
        self.assertSetEqual(state.epsilon_paths(), set([1, 2]))

    def test_prints_string(self):
        expected = "NFAState: 1 Paths: 2, 3||"
        state = NFAState(1)
        epsilon = TransitionStub(set(), "epsilon", True)
        normal_transition = TransitionStub(set(['a']), "char: a")
        state.add_path(epsilon, NFAState(2))
        state.add_path(normal_transition, NFAState(3))
        self.assertEqual(expected, str(state))
