import unittest as ut
from collections import namedtuple
import copy
from inspect import isclass


TransitionEntry = namedtuple('TransitionEntry', ['marked_transitions',
                             'epsilon_transitions'])


class NFA:
    """ Holds all transitions required for traversing the NFA """

    # The default "empty" automata
    empty_nfa_table = {0: TransitionEntry({}, [1]), 1: TransitionEntry({}, [])}

    def __init__(self, transition_table=None, start=0, final=1):
        self._transition_table = transition_table if transition_table \
                                 else self.empty_nfa_table
        self._start_node = start
        self._end_node = final

    # Given a state and transition_char, returns the next possible transition
    # or returns "None" if there is not one
    def marked_transition(self, node_id, input_char):
        transitions = self._transition_table.get(node_id, None)

        # Try returning something else here: Maybe try/catch an exception and
        # log the entire nfa before quitting the method
        if transitions is None:
            print("Invalid NodeID: ", node_id, " Corrupt nfa")
            return None
        return transitions.marked_transitions.get(input_char, None)

    # Returns a list of node_ids representing all possible "free" transitions
    # (epsilons) from node_id. Returns an empty list if there are none
    def epsilon_transitions(self, node_id):
        transitions = self._transition_table.get(node_id, None)
        if transitions is None:
            print("Invalid NodeID: ", node_id)
        return transitions.epsilon_transitions


class NFATest(ut.TestCase):
    def setUp(self):
        self.transition_table = {
            0: TransitionEntry({}, [1, 2]),
            1: TransitionEntry({}, [3, 7]),
            2: TransitionEntry({'c': 7}, []),
            3: TransitionEntry({'a': 5}, []),
            4: TransitionEntry({}, [8]),
            5: TransitionEntry({'b': 6}, []),
            6: TransitionEntry({}, [3, 7]),
            7: TransitionEntry({}, [8]),
            8: TransitionEntry({}, [])
        }

    def test_retrieves_existent_marked_transition(self):
        nfa = NFA(self.transition_table, start=0, final=8)
        next_node = nfa.marked_transition(node_id=3, input_char='a')
        self.assertEqual(next_node, 5)

    def test_non_existent_node_access(self):
        nfa = NFA(self.transition_table, start=0, final=8)
        next_node = nfa.marked_transition(0, 'a')
        self.assertIsNone(next_node)

    def test_get_epsilons(self):
        nfa = NFA(self.transition_table, start=0, final=8)
        epsilons = nfa.epsilon_transitions(node_id=6)
        self.assertEqual(epsilons, [3, 7])

    def test_object_is_immutable(self):
        pass


class NFAIterator:
    # Iterators keep track of the NFA's "partial state", creating child
    # on each possible transition.
    def __init__(self, start_node):
        self._current_node = start_node
        self._history = []

    def spawn_child(self, next_state, transition=None):
        child = NFAIterator(next_state)
        child._history = self._history.copy()
        if transition:
            child._history.append(transition)
        return child

    def history_length(self):
        return len(self._history)


"""
State() .add(NFAIterator), iterable, makes sure only the one with the longest
history is the one that survives
Question: Should it be the iterators job to manage whether a state is valid or
not???
"""


def longer_history(iter1, iter2):
    return iter1 if iter1.history_length() > iter2.history_length() \
           else iter2


class NFAState:
    def __init__(self):

        # states_held holds all of the active NFAIterators which can be looked
        # up by the node_id of the state they hold
        self._states_held = {}

    def __iter__(self):
        return iter(self._states_held.values())

    def add(self, iterator):
        node = iterator.current_node
        if node in self._states_held:
            other = self._states_held[node]
            self._states_held[node] = longer_history(iterator, other)
        else:
            self._states_held[node] = iterator


class NFAStateTest(ut.TestCase):
    def test_only_allows_one_iterator_per_state(self):
        mock_iter1 = type("MockIter", (), {'history_length': lambda: 4,
                          'current_node': 1})
        mock_iter2 = type("MockIter", (), {'history_length': lambda: 5,
                          'current_node': 1})
        mock_iter3 = type("MockIter", (), {'history_length': lambda: 6,
                          'current_node': 2})
        mock_iter4 = type("MockIter", (), {'history_length': lambda: 7,
                          'current_node': 3})

        state = NFAState()
        state.add(mock_iter1)
        state.add(mock_iter2)
        state.add(mock_iter3)
        state.add(mock_iter4)
        expected_state = [mock_iter2, mock_iter3, mock_iter4]
        for iterator in state:
            self.assertTrue(iterator in expected_state)
            expected_state.remove(iterator)
        self.assertListEqual(expected_state, [])

        # define two mock iterators with staees and histories the latter of
        # which should be a method


class NFASimulator:
    def __init__(self, nfa, state_container):
        self._nfa = nfa
        self._start_id = self._nfa._start_node
        self._final_id = self._nfa._end_node
        assert(isclass(state_container))
        self._state_container = state_container
        self._state = self._state_container()

    # Takes a str as input and puts the input into the automata char by char
    # Returns a list of all the input iterators that ends up in the final node
    def cycle_state(self, input_str):
        next_state = self._state_container.new()
        print(next_state)

    def reset_state(self):
        self._state = self._state_container()

    def _compute_epsilon_closure(self, start_iter):
        # Uses dfs to search the nfa and spawn a new nfa_iter for each new
        # epsilon closure
        # ##NOTE: Here, to optimize, we need to make sure not only that a path
        #         has not been explored in the local search, but that an iter
        #         has not also already been made on it in the global
        #         state...
        #         IDEA: Create an node_iter cache...that holds the epsilon
        #         closure of a bunch of different nodes in the cache
        pass

    def single_cycle():
        pass


class NFASimulatorTest(ut.TestCase):
    def setUp(self):
        self.transition_table = {
                0: TransitionEntry({}, [1, 2]),
                1: TransitionEntry({}, [3, 7]),
                2: TransitionEntry({'c': 7}, []),
                3: TransitionEntry({'a': 5}, []),
                4: TransitionEntry({}, [8]),
                5: TransitionEntry({'b': 6}, []),
                6: TransitionEntry({}, [3, 7]),
                7: TransitionEntry({}, [8]),
                8: TransitionEntry({}, [])
                }
        self.nfa_mock = NFA(self.transition_table, 0, 8)

    def test_treats_strings_and_char_input_identically(self):
        nfa = self.nfa_mock
        sim1 = NFASimulator(nfa)
        sim2 = copy.deep_copy(sim1)
        self.assertListEqual(sim1.cycle('abc'), [sim2.cycle(c) for c in 'abc'])

    def test_returns_iterators_when_in_final_state(self):
        pass


if __name__ == '__main__':
    ut.main()
