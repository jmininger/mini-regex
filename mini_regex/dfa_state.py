import bisect


class NFAIterator:
    """ Represents a singular "alive" state in an nfa. The substate represents
    a single node in the nfa/graph, while the age represents the number of
    "input-chars" that the iterator has eaten from the input string
    """

    def __init__(self, node, age):
        self.node = node
        self.age = age

    def __repr__(self):
        return "Age: " + str(self.age) + " node: " + str(self.node)

    def __eq__(self, other):
        return self.age == other.age and self.node.id == other.node.id

    def __lt__(self, other):
        return self.age < other.age

    def get_node(self):
        return self.node

    def get_age(self):
        return self.age


class DFAState:
    """ A set of NFAIterators that, when together, represent the state of the
    automata given a starting position in a search string. Does not contain
    identical substates.
    """
    def __init__(self):
        # List of active iterators all sorted by age
        self.partial_states = []

    def __repr__(self):
        return str(self.partial_states)

    def add_substate(self, substate):
        bisect.insort_right(self.partial_states, substate)

    def get_substate_with_node(self, node):
        for substate in self.partial_states:
            if substate.node == node:
                return substate
        return None

    def get_substates(self):
        return self.partial_states

    # def substates_with_age(self, age):
    #     idx = self.partial_states.index(age)
    #     last_index = (len(self.partial_state) -
    #                   self.partial_states[::-1].index(age))
    #     return self.partial_states[idx:last_index]
