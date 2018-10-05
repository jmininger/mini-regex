import unittest as ut


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


class NFATest(ut.TestCase):
    min_trans_table = {
            0: ([], [1]),
            1: ([], [])
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


if __name__ == '__main__':
    ut.main()
