import unittest as ut
from inspect import isclass
import logging
from util import Stack, table_to_nfa

logging.basicConfig(filename='log.txt', filemode='w', level=logging.DEBUG)


class NFATest(ut.TestCase):
    def test_single_char_match(self):
        nfa = table_to_nfa({0: ({'a': 1}, []), 1: ({}, [2]), 2: ({}, [])},
                           start=0, end=2)
        nfa.cycle()
        self.assertEqual(nfa.num_matches(), 0)
        self.assertListEqual(nfa.prev_matches(), [])


class DFA:
    pass
# class NFATest(ut.TestCase):
#     def setUp(self):
#         self.transition_table = {
#             0: TransitionEntry({}, [1, 2]),
#             1: TransitionEntry({}, [3, 7]),
#             2: TransitionEntry({'c': 7}, []),
#             3: TransitionEntry({'a': 5}, []),
#             4: TransitionEntry({}, [8]),
#             5: TransitionEntry({'b': 6}, []),
#             6: TransitionEntry({}, [3, 7]),
#             7: TransitionEntry({}, [8]),
#             8: TransitionEntry({}, [])
#         }

#     def test_retrieves_existent_marked_transition(self):
#         nfa = NFA(self.transition_table, start=0, final=8)
#         next_node = nfa.marked_transition(node_id=3, input_char='a')
#         self.assertEqual(next_node, 5)

#     def test_impossible_transition(self):
#         nfa = NFA(self.transition_table, start=0, final=8)
#         next_node = nfa.marked_transition(0, 'a')
#         self.assertIsNone(next_node)

#     def test_retrieves_epsilons(self):
#         nfa = NFA(self.transition_table, start=0, final=8)
#         epsilons = nfa.epsilon_transitions(node_id=6)
#         self.assertEqual(epsilons, [3, 7])

#     def test_empty_list_when_no_epsilons(self):
#         nfa = NFA(self.transition_table, final=8)
#         epsilons = nfa.epsilon_transitions(5)
#         self.assertListEqual(epsilons, [])

#     def test_raises_exception_on_invalid_node_access(self):
#         nfa = NFA(self.transition_table, final=8)
#         self.assertRaises(Exception, nfa.marked_transition, -1, 'a')

#     def test_raises_exception_on_invalid_node(self):
#         nfa = NFA(self.transition_table, final=8)
#         self.assertRaises(Exception, nfa.epsilon_transitions, -1)

#     def test_constructs_empty_nfa_when_none_specified(self):
#         nfa = NFA()
#         self.assertListEqual(nfa.epsilon_transitions(0), [1])
#         self.assertListEqual(nfa.epsilon_transitions(1), [])


# class NFAIterator:
#     """ NFAIterators are used to represent a single state during an NFA
#         simulation. It is also in charge of tracking the characters it has
#         consumed to reach the state that it is in """

#     def __init__(self, node_id):
#         self._current_node = node_id
#         self._history = []  # ordered list of all chars the iter has consumed

#     def __str__(self):
#         return "".join([
#                     "NODE: ", str(self._current_node),
#                     " History: ", ",".join(self._history)
#                 ])

#     @property
#     def history(self):
#         return self._history

#     @property
#     def node(self):
#         return self._current_node

#     def spawn_child(self, next_state, input_symbol=None):
#         """ Creates a new iterator that copies the old one over and advances
#             the state of the iterator """
#         child = NFAIterator(next_state)
#         child._history = self._history.copy()

#         # Epsilon transitions do not effect an iterator's symbol history
#         if input_symbol:
#             child._history.append(input_symbol)
#         return child

#     def history_length(self):
#         return len(self._history)


# class NFAIteratorTest(ut.TestCase):
#     def test_iters_keep_track_of_history_on_spawn(self):
#         parent = NFAIterator(1)
#         child1 = parent.spawn_child(2, 'a')
#         child2 = child1.spawn_child(3, 'b')
#         child3 = child2.spawn_child(4, 'c')
#         child4 = child2.spawn_child(5)
#         self.assertListEqual(child3.history, ['a', 'b', 'c'])
#         self.assertListEqual(child4.history, ['a', 'b'])

#     def test_retrieves_current_node(self):
#         iter1 = NFAIterator(0)
#         self.assertEqual(iter1.spawn_child(4).node, 4)


# def longer_history(iter1, iter2):
#     return iter1 if iter1.history_length() > iter2.history_length() \
#            else iter2


# class NFAStateContainer:
#     """ Serves as a set data structure containing all of the partial states
#         (iterators) that an NFA is in during a single cycle. If a state is
#         added, this container will make sure that if there is currently another
#         iter on the same node, only the iter with the longer history will
#         remain"""

#     def __init__(self):
#         # Holds all active NFAIterators for a cycle
#         # Key: Node_id, Value: NFAIterator
#         self._states_held = {}

#     def __str__(self):
#         return "".join(["NFAState: ", ",".join([str(nfa_iter) for nfa_iter in
#                         self._states_held.values()])])

#     def __iter__(self):
#         """ Allows iteration over all states """
#         return iter(self._states_held.values())

#     def add(self, *states):
#         for state in states:
#             # When two iterators end up on the same node, their futures
#             # will be identical, so there is no point in tracking both of
#             # them. In this case, we choose to drop the iter with the
#             # shorter history
#             conflicting_state = self._states_held.get(state.node)
#             if conflicting_state:
#                 self._states_held[state.node] = \
#                      longer_history(state, conflicting_state)
#             else:
#                 self._states_held[state.node] = state

#     def get_state_at(self, node_id):
#         return self._states_held.get(node_id)


# class NFAStateTest(ut.TestCase):
#     def setUp(self):
#         self.mock_iter1 = type("MockIter", (), {'history_length': lambda: 4,
#                                'node': 1})
#         self.mock_iter2 = type("MockIter", (), {'history_length': lambda: 5,
#                                'node': 1})
#         self.mock_iter3 = type("MockIter", (), {'history_length': lambda: 6,
#                                'node': 2})
#         self.mock_iter4 = type("MockIter", (), {'history_length': lambda: 7,
#                                'node': 3})

#     def test_only_allows_one_iterator_per_state(self):
#         state = NFAStateContainer()
#         state.add(self.mock_iter1)
#         state.add(self.mock_iter2)
#         state.add(self.mock_iter3)
#         state.add(self.mock_iter4)
#         expected_state = [self.mock_iter2, self.mock_iter3, self.mock_iter4]
#         for iterator in state:
#             self.assertTrue(iterator in expected_state)
#             expected_state.remove(iterator)
#         self.assertListEqual(expected_state, [])

#     def test_access_current_states(self):
#         # Observer pattern here?
#         state = NFAStateContainer()
#         state.add(self.mock_iter1)
#         state.add(self.mock_iter2, self.mock_iter3, self.mock_iter4)
#         nfa_iter = state.get_state_at(3)
#         self.assertEqual(nfa_iter, self.mock_iter4)

#     def test_returns_none_on_empty_nodes(self):
#         state = NFAStateContainer()
#         state.add(self.mock_iter1, self.mock_iter2,
#                   self.mock_iter3, self.mock_iter4)
#         non_existent_iter = state.get_state_at(0)
#         self.assertIsNone(non_existent_iter)


# class NFASimulator:
#     """ Takes an NFA graph, and uses it to transition and hold state based
#         input """

#     def __init__(self, nfa, state_container, state_iterator):
#         # state_container, and state_iterator are classes used to construct
#         # elements in the simulator. This use of dependency injection (enabled
#         # by the use of interfaces and not direct objects) allows for easier
#         # testing and different strategies later on
#         self._nfa = nfa
#         self._start_id = self._nfa._start_node
#         self._final_id = self._nfa._end_node

#         assert(isclass(state_container))
#         self._state_container = state_container
#         self._state = self._state_container()
#         assert(isclass(state_iterator))
#         self._state_iterator = state_iterator

#     def _compute_epsilon_closure(self, parent_iter):
#         """ Returns a list of NFAIterators
#             Uses DFS to search the nfa for all possible "free"(epsilon)
#             transitions that can be made from the parent_iter """
#         explored = set()
#         frontier = Stack()
#         frontier.push(parent_iter.node)
#         while frontier:
#             node = frontier.pop()
#             explored.add(node)
#             epsilons = self._nfa.epsilon_transitions(node)
#             frontier.push(*[n for n in epsilons if n not in explored])

#         # Create iters for each epsilon and have each inherit the parent's
#         # history
#         return [parent_iter.spawn_child(node) for node in explored]

#     def cycle_state(self, symbol):
#         """ Completes one cycle through the NFA, passing in a char and
#             recieving any state that ... """
#         # Initialize the state
#         next_state = self._state_container()

#         start_iter = self._state_iterator(self._start_id)
#         next_state.add(start_iter)
#         epsilon_iters = self._compute_epsilon_closure(start_iter)
#         next_state.add(*epsilon_iters)

#         for iterator in self._state:
#             next_node = self._nfa.marked_transition(iterator.node, symbol)
#             if next_node:
#                 child_iter = iterator.spawn_child(next_node, symbol)
#                 next_state.add(child_iter)
#                 epsilon_iters = self._compute_epsilon_closure(child_iter)
#                 next_state.add(*epsilon_iters)

#         self._state = next_state
#         return self._state.get_state_at(self._final_id)

#     def reset_state(self):
#         self._state = self._state_container()


# class NFASimulatorTest(ut.TestCase):
#     def setUp(self):
#         # represents the pattern: d(ab|c*)
#         self.transition_table = {
#                 0: TransitionEntry({'d': 9}, []),
#                 9: TransitionEntry({}, [1, 2]),
#                 1: TransitionEntry({}, [3, 7]),
#                 2: TransitionEntry({'c': 7}, []),
#                 3: TransitionEntry({'a': 5}, []),
#                 4: TransitionEntry({}, [8]),
#                 5: TransitionEntry({'b': 6}, []),
#                 6: TransitionEntry({}, [3, 7]),
#                 7: TransitionEntry({}, [8]),
#                 8: TransitionEntry({}, [])
#                 }
#         self.nfa_mock = NFA(self.transition_table, 0, 8)
#         self.state_container = NFAStateContainer
#         self.state_iterator = NFAIterator
#         self.epsilon_only_transitions = {
#                 0: TransitionEntry({}, [1, 2]),
#                 1: TransitionEntry({}, [3, 5]),
#                 2: TransitionEntry({}, []),
#                 3: TransitionEntry({'a': 4}, []),
#                 4: TransitionEntry({}, []),
#                 5: TransitionEntry({}, [5])
#             }

#     def test_computes_epsilon_closure_on_empty_string(self):
#         nfa = NFA(self.epsilon_only_transitions, 0, 5)
#         sim = NFASimulator(nfa, self.state_container, self.state_iterator)
#         match = sim.cycle_state('')
#         self.assertEqual(str(match), str(NFAIterator(5)))

#     def test_properly_identifies_matches(self):
#         sim = NFASimulator(self.nfa_mock, self.state_container,
#                            self.state_iterator)
#         self.assertIsNone(sim.cycle_state('a'), None)
#         self.assertListEqual(sim.cycle_state('d').history, ['d'])

    # def test_handles_infinite_node_transition(self):
    #     """ Infinity is the name I give the scenario where a node has an
    #         epsilon transition to itself and so the node is always part of
    #         the NFA's state """
    #     infinity_nfa_table = {
    #                 0: TransitionEntry({'a': 1}, []),
    #                 1: TransitionEntry({'b': 2}, [1]),
    #                 2: TransitionEntry({}, [])
    #             }
    #     state_mock = type('NFAStateContainer', {

    #         })
    #   sim = NFASimulator(NFA(infinity_nfa_table, 0, 2), self.state_container,
    #                        self.state_iterator)
    #     sim.cycle_state('a')
    #     match = sim.cycle_state('c')

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
