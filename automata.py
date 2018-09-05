import unittest as ut
from collections import namedtuple
from inspect import isclass
import logging

from stack import Stack

logging.basicConfig(filename='log.txt', filemode='w', level=logging.DEBUG)
# TransitionEntry organizes data stored in an NFA's transition table
# marked_transitions = dict('input_char': 'node_id'})
# epsilon_transitions = list(node_id)
TransitionEntry = namedtuple('TransitionEntry', ['marked_transitions',
                             'epsilon_transitions'])


class NFA:
    """ Holds all transitions required for traversing the NFA. This structure
        is immutable once created by the Builder """

    # The default "empty" automata
    empty_nfa_table = {0: TransitionEntry({}, [1]), 1: TransitionEntry({}, [])}

    def __init__(self, transition_table=None, start=0, final=1):
        # Holds the graph representing the NFA
        self._start_node = start
        self._end_node = final
        if transition_table:
            self._transition_table = transition_table
        else:
            self._transition_table = NFA.empty_nfa_table

    def __str__(self):
        table = []
        for node_id, trans in self._transition_table.items():
            table.append(
                "NodeID: " + str(node_id) +
                " Transitions: " + str(trans)
            )
        table = "\n".join(table)

        return "".join([
                    "StartNode: ", str(self._start_node),
                    ", FinalNode: ", str(self._end_node),
                    "\nTableRepr: ", table
                ])

    def marked_transition(self, node_id, input_char):
        """ Given a state and transition_char, returns the next possible transition
            or returns "None" if there is not one """
        transition_entry = self._transition_table.get(node_id, None)
        if transition_entry is None:
            logging.error("MarkedTransition Invalid NodeID: " + str(node_id))
            raise Exception("CorruptNFA")
        return transition_entry.marked_transitions.get(input_char, None)

    def epsilon_transitions(self, node_id):
        """ Returns a list of node_ids representing all possible
            "free" transitions (epsilons) from node_id. Returns an
            empty list if there are none """
        transition_entry = self._transition_table.get(node_id, None)
        if transition_entry is None:
            logging.error("MarkedTransition Invalid NodeID: " + str(node_id))
            raise Exception("CorruptNFA")
        return transition_entry.epsilon_transitions


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

    def test_impossible_transition(self):
        nfa = NFA(self.transition_table, start=0, final=8)
        next_node = nfa.marked_transition(0, 'a')
        self.assertIsNone(next_node)

    def test_retrieves_epsilons(self):
        nfa = NFA(self.transition_table, start=0, final=8)
        epsilons = nfa.epsilon_transitions(node_id=6)
        self.assertEqual(epsilons, [3, 7])

    def test_empty_list_when_no_epsilons(self):
        nfa = NFA(self.transition_table, final=8)
        epsilons = nfa.epsilon_transitions(5)
        self.assertListEqual(epsilons, [])

    def test_raises_exception_on_invalid_node_access(self):
        nfa = NFA(self.transition_table, final=8)
        self.assertRaises(Exception, nfa.marked_transition, -1, 'a')

    def test_raises_exception_on_invalid_node(self):
        nfa = NFA(self.transition_table, final=8)
        self.assertRaises(Exception, nfa.epsilon_transitions, -1)

    def test_constructs_empty_nfa_when_none_specified(self):
        nfa = NFA()
        self.assertListEqual(nfa.epsilon_transitions(0), [1])
        self.assertListEqual(nfa.epsilon_transitions(1), [])


class NFAIterator:
    # Iterators keep track of the NFA's "partial state", creating child
    # on each possible transition.
    def __init__(self, start_node):
        self._current_node = start_node
        self._history = []

    def __str__(self):
        return "".join(["NODE: ", str(self._current_node), " History: ",
                        ",".join([str(elem) for elem in self._history])])

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

    def add(self, *iterators):
        for iterator in iterators:
            node = iterator._current_node
            if node in self._states_held:
                other = self._states_held[node]
                self._states_held[node] = longer_history(iterator, other)
            else:
                self._states_held[node] = iterator

    def __str__(self):
        return "".join(["NFAState: ", ",".join([str(nfa_iter) for nfa_iter in
                        self._states_held.values()])])


class NFAStateTest(ut.TestCase):
    def setUp(self):
        self.mock_iter1 = type("MockIter", (), {'history_length': lambda: 4,
                               '_current_node': 1})
        self.mock_iter2 = type("MockIter", (), {'history_length': lambda: 5,
                               '_current_node': 1})
        self.mock_iter3 = type("MockIter", (), {'history_length': lambda: 6,
                               '_current_node': 2})
        self.mock_iter4 = type("MockIter", (), {'history_length': lambda: 7,
                               '_current_node': 3})

    def test_only_allows_one_iterator_per_state(self):

        state = NFAState()
        state.add(self.mock_iter1)
        state.add(self.mock_iter2)
        state.add(self.mock_iter3)
        state.add(self.mock_iter4)

        # mock_iter1 is not expected to be in the final state because it
        # matches the same part of the string as mock_iter2, but the match
        # spans less of the string than mock_iter2
        expected_state = [self.mock_iter2, self.mock_iter3, self.mock_iter4]
        for iterator in state:
            self.assertTrue(iterator in expected_state)
            expected_state.remove(iterator)
        self.assertListEqual(expected_state, [])


class NFASimulator:
    def __init__(self, nfa, state_container, state_iterator):
        # state_container, and state_iterator are classes used to construct
        # elements in the simulator. This use of dependency injection (enabled
        # by the use of interfaces and not direct objects) allows for easier
        # testing and different strategies later on
        self._nfa = nfa
        self._start_id = self._nfa._start_node
        self._final_id = self._nfa._end_node
        assert(isclass(state_container))
        self._state_container = state_container
        self._state = self._state_container()
        assert(isclass(state_iterator))
        self._state_iterator = state_iterator
        # Initialize the state
        start_iter = self._state_iterator(self._start_id)
        self._state.add(start_iter)
        self._state.add(*self._compute_epsilon_closure(start_iter))
    # Takes a str as input and puts the input into the automata char by char
    # Returns a list of all the input iterators that ends up in the final node

    def cycle_state(self, input_str):
        # Make iter for start state, use this to spawn iterators for the
        # computed epsilon closure
        # Then for each element in the current state, attempt to advance,
        # for each state successful in advancing, compute epsilon closure and
        # spawn new nodes for each of these
        matches = []
        for input_char in input_str:
            next_state = self._state_container()
            start_iter = self._state_iterator(self._start_id)
            next_state.add(start_iter)
            next_state.add(*self._compute_epsilon_closure(start_iter))
            for node_iter in self._state:
                # clean this up...it is super sloppy
                next_node = self._nfa.marked_transition(
                                 node_iter._current_node, input_char)

                advance_iter = node_iter.spawn_child(next_node, input_char)
                if advance_iter:
                    next_state.add(advance_iter)
            # Make more legible by update_state(next_state)
            self._state = next_state

            # These two lines retrieve any iters in the final state
            matches.append(self._state._states_held.get(self._final_id, []))
        matches.append(self._state._states_held.get(self._final_id, []))
        return matches

    def reset_state(self):
        self._state = self._state_container()

    def _compute_epsilon_closure(self, start_iter):
        # Returns a list of NFAIterators
        # Uses DFS to search the nfa for all possible "free"(epsilon)
        # transitions that can be made from start_iter
        explored = set()
        frontier = Stack()
        frontier.push(start_iter._current_node)
        while frontier:
            node = frontier.pop()
            explored.add(node)
            frontier.push(*[n for n in self._nfa.epsilon_transitions(node)
                            if n not in explored])
        return [start_iter.spawn_child(node) for node in explored]


class NFASimulatorTest(ut.TestCase):
    def setUp(self):
        self.transition_table = {
                0: TransitionEntry({'d': 9}, []),
                9: TransitionEntry({}, [1, 2]),
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
        self.state_container = NFAState
        self.state_iterator = NFAIterator

    def test_computes_epsilon_closure_on_empty_string(self):
        sim = NFASimulator(self.nfa_mock, self.state_container,
                           self.state_iterator)
        matches = sim.cycle_state('')
        self.assertEqual(len(matches), 1)

    # def test_returns_all_matches_in_str(self):
    #     pass
    #     sim = NFASimulator(self.nfa_mock, self.state_container,
    #                        self.state_iterator)
    #     matches = sim.cycle_state('dedacabc')
    #     self.assertEqual(", ".join([str(m) for m in matches]), "")
    #     self.assertEqual(str(sim._state), '')
    #     self.assertEqual(len(matches), 3)
#     def test_treats_strings_and_char_input_identically(self):
#         nfa = self.nfa_mock
#         sim1 = NFASimulator(nfa)
#         sim2 = copy.deep_copy(sim1)
#         self.assertListEqual(sim1.cycle('abc'), [sim2.cycle(c) for c in \
        # 'abc'])

#     def test_returns_iterators_when_in_final_state(self):
#         pass


if __name__ == '__main__':
    ut.main()
