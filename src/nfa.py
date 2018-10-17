import stack


class State:
    """ A state is nothing more than an ID and a list of
        transition -> node pairs """

    def __init__(self, id):
        self.id = id
        self.paths = []

    def add_path(self, transition, destination):
        path = (transition, destination)
        self.paths.append(path)

    def available_paths(self, char):
        return [destination for transition, destination in self.paths if
                transition.is_available(char)]

    def epsilon_paths(self):
        return self.available_paths('')


class NFA:  # Rename to NFAGraph?
    def __init__(self, trans_table, start_state, end_states):
        self._table = trans_table

        # Ensure that start_state and end_states are part of the automata
        if start_state not in trans_table:
            raise Exception('start state is not a valid state')
        self._start_state = start_state
        if not all([(state in self._table) for state in end_states]):
            raise Exception('end states are not all valid states')
        self._end_states = end_states

    def get_state(self, state_id):
        if state_id not in self._table:
            raise Exception('invalid state id: ', state_id)
        return self._table[state_id]

    def get_epsilon_transition(self, state_id):
        state = self.get_state(state_id)
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
        """ Runs a simple DFS on the nfa using only epsilon transitions from
        the start state """
        # TODO: Add a closure cache
        #   Extract function from class and make it normal function

        explored = set()  # TODO: Make this a bitmap
        frontier = stack.Stack()
        has_cycle_at_start = False
        state = self.get_state(state_id)
        start_states = state.get_epsilon_transition()
        frontier.push(start_states)

        while not frontier.is_empty():
            state = self.get_state(frontier.top())
            frontier.pop()
            epsilons = self.get_epsilon_transition(state.id)
            for epsilon in epsilons:
                if epsilon not in explored:
                    frontier.push(epsilon)
                if epsilon == state_id:
                    has_cycle_at_start = True
            explored.add(state.id)

        # If a node has been explored, it belongs in the epsilon closure
        # with the exception of the start node. The start node should only
        # remain in the closure if it can be reached from any other node in the
        # closure (creating a cycle)
        if not has_cycle_at_start:
            explored.remove(state_id)
        return explored

    def is_final_state(self, state_id):
        return state_id in self.end_states


# Should the iterators be able to plug any value into the state machine? Does
# this make sense?
# Should calculate next
# Should automatically calculate the epsilon closure and take care of
#  any cycles in the graph
# Should be easy to compose
# StateStub -> Rewrite the available_paths() func to return one elem on
# epsilons and to return another on the other fake input
# TODO:
# add test making sure epsilon cycles terminate and dont cause infinite loop
# Add a is_final_state(nodes)
# Given a node_id and the next character, return the next state
#   - If there is no next state, should we return "None" or the start state?
# Need a way to store transition entries
#   - Cannot represent transitions as chars, they need to be token classes
