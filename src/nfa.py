import unittest as ut
import transitions
import stack


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

    def get_state(self, state_id):
        if state_id not in self._table:
            raise Exception('invalid state id: ', state_id)
        return self._table[state_id]

    def get_epsilon_transition(self, state_id):
        state = self.get_state(self, state_id)
        return state.available_paths('')

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

    def epsilon_closure(self, state_id):
        # Ideas: Add a closure cache
        #   Extract function from class and make it normal function
        explored = set()
        frontier = stack.Stack()
        state = self.get_state(state_id)
        frontier.push(state.id)
        while not frontier.


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


# table = {1: State(1),
# @ut.skip('')
class NFATest(ut.TestCase):
    min_trans_table = {
            0: StateStub(0, {'': 1}),
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
                0: StateStub({}, [1, 2]),
                1: StateStub(1, {'a': [5], '': [4]}),
                2: StateStub(2, {'': 3}),
                3: StateStub(3, {'': 1}),
                4: StateStub(4, {}),
                5: StateStub(5, {'': [6]}),
                6: StateStub(6, {'': [1]})
                }
        nfa = NFA(trans_table, 0, [4])
        # Makes sure that a closure does not include itself
        # self.assertSetEqual(epsilon_closure0, set([0, 2, 3, 4]))
        epsilon_closure0 = nfa.epsilon_closure(0)
        self.assertSetEqual(epsilon_closure0, set([0, 2, 3, 4]))

        epsilon_closure4 = nfa.epsilon_closure(4)
        self.assertSetEqual(epsilon_closure4, set([]))

        epsilon_closure5 = nfa.epsilon_closure(5)
        self.assertSetEqual(epsilon_closure5, set([1, 2, 3, 4, 5, 6]))
# Should calculate next
# Should automatically calculate the epsilon closure and take care of
#  any cycles in the graph
# Should be easy to compose
# StateStub -> Rewrite the available_paths() func to return one elem on
# epsilons and to return another on the other fake input

# TODO:
# Add a is_final_state(nodes)
# Given a node_id and the next character, return the next state
#   - If there is no next state, should we return "None" or the start state?
# Need a way to store transition entries
#   - Cannot represent transitions as chars, they need to be token classes
if __name__ == '__main__':
    ut.main()
