import unittest as ut
import transitions


class State:
    """ A state is nothing more than an ID and a list of
        transition -> node pairs """

    def __init__(self, id):
        self.id = id
        self.paths = []

    def add_path(self, transition, next_state):
        path = (transition, next_state)
        self.paths.append(path)

    def available_paths(self, char):
        return [state for transition, state in self.paths if
                transition.is_available(char)]


class TransitionStub(transitions.Transition):
    def __init__(self, available_set):
        self.available_set = available_set

    def is_available(self, char):
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


class NFA:
    def __init__(self, trans_table, start_state, end_states):
        self._table = trans_table

        # Ensure that start_state is part of the automata
        if start_state not in trans_table:
            raise Exception('start state is not a valid state')
        self._start_state = start_state

        # Ensure that all end_states are part of the automata
        if not all([(state in self._table) for state in end_states]):
            raise Exception('end states are not all valid states')
        self._end_states = end_states

    def get_epsilon_transition(self, state_id):
        pass

    @property
    def end_states(self):
        return self._end_states

    @property
    def start_state(self):
        return self._start_state

    # @start_state.setter
    # def start_state(self, val):
    #     """ TODO: Can this method be private? We don't want it accessed by
    #         clients; only the constructor should use it """

    #     if val not in self._table:
    #         raise Exception('start state is not a valid state')
    #     self.__start_state = val

    def epsilon_closure(self, state):
        return self._table.epsilons(state)


# @ut.skip('')
class NFATest(ut.TestCase):
    min_trans_table = {
            0: ({}, [1]),
            1: ({}, [])
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
                0: ({}, [1, 2]),
                1: ({'a': 5}, [4]),
                2: ({}, [3]),
                3: ({}, [1]),
                4: ({}, []),
                5: ({}, [6]),
                6: ({}, [1])
                }
        nfa = NFA(trans_table, 0, [4])
        # Makes sure that a closure does not include itself
        epsilon_closure0 = nfa.epsilon_closure(0)
        self.assertSetEqual(epsilon_closure0, set([1, 2, 3, 4]))

        epsilon_closure4 = nfa.epsilon_closure(4)
        self.assertSetEqual(epsilon_closure4, set([]))

        epsilon_closure5 = nfa.epsilon_closure(5)
        self.assertSetEqual(epsilon_closure5, set([1, 2, 3, 4, 5, 6]))


# TODO:
# Add a is_final_state(nodes)
# Given a node_id and the next character, return the next state
#   - If there is no next state, should we return "None" or the start state?
# Need a way to store transition entries
#   - Cannot represent transitions as chars, they need to be token classes
if __name__ == '__main__':
    ut.main()
