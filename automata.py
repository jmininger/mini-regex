import unittest as ut
from collections import namedtuple


TransitionEntry = namedtuple('TransitionEntry', ['marked_transitions',
                             'epsilon_transitions'])


class NFA:
    empty_nfa_table = {0: TransitionEntry({}, [1]), 1: TransitionEntry({}, [])}

    def __init__(self, transition_table=None, start=0, final=1):
        self._transition_table = transition_table if transition_table \
                                 else self.empty_nfa_table
        self._start_node = start
        self._end_node = final

    def marked_transition(self, node_id, input_char):
        transitions = self._transition_table.get(node_id, None)

        # Try returning something else here: Maybe try/catch an exception and
        # log the entire nfa before quitting the method
        if transitions is None:
            print("Invalid NodeID: ", node_id, " Corrupt nfa")
            return None
        return transitions.marked_transitions.get(input_char, None)

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


# Nfasim.get_epsilon_transition(node_id)


if __name__ == '__main__':
    ut.main()
