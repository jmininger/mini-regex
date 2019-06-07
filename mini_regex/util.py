from collections import deque
from enum import Enum
from mini_regex.nfa import NFAState, NFA
from mini_regex.transitions import (create_char_trans,
                                    create_epsilon_trans,
                                    create_metachar_trans)


class TransitionTypes(Enum):
    CHAR = 1
    EPSILON = 2
    CLASS = 3


# Table = { StateID: [Transitions] }
#   where Transition = (TransitionDesc, NextStateID)
# { id: [("epsilon", someOtherID), ("char: b", otherID)] }


def table_to_nfa(table, start_state, end_state):
    state_table = {id: NFAState(id) for id in table}
    for id, trans in table.items():
        state = state_table[id]
        for edge in trans:
            desc_str, dst_id = edge
            trans_val = trans_desc_to_trans(desc_str)
            state.add_path(trans_val, state_table[dst_id])
    return NFA(state_table[start_state], state_table[end_state])


def trans_desc_to_trans(desc_str):
    if desc_str == "epsilon":
        return create_epsilon_trans()
    elif desc_str == "metachar":
        return create_metachar_trans()
    elif desc_str[0:6] == "char: ":
        return create_char_trans(desc_str[6])
    else:
        Exception("cannot convert " + desc_str + " to a transition")


class Stack:
    """ Wrapper class around deque that only allows
        user to push/pop on the right
    """

    def __init__(self, iterable=[]):
        self._deque = deque(iterable)

    def __iter__(self):
        while self._deque:
            yield self.pop()

    def __len__(self):
        return len(self._deque)

    def pop(self):
        return self._deque.pop()

    def top(self):
        return self._deque[-1]

    def push(self, *args):
        for elem in args:
            self._deque.append(elem)

    def is_empty(self):
        return len(self) == 0


class Counter:

    """ Responsible for providing each state with a unique_id. Not all states
    are initialized at the same time, or even in the same scope, so it makes
    sense to have an allocator that keeps track of which numbers have been used
    """

    def __init__(self):
        # Start at -1 so the first number produced is 0
        self._num = -1

    def next(self):
        self._num += 1
        return self._num


def nfa_to_table(nfa_start):
    """ Makes it easier to visualize an nfa and manually check its accuracy
    Uses a dfs strategy to construct the table
    """
    explored = set()
    frontier = Stack()
    table = {}
    frontier.push(nfa_start)
    explored.add(nfa_start.id)

    while not frontier.is_empty():
        state = frontier.top()
        frontier.pop()
        paths = [
            (str(trans), dst.id)
            for trans, dst in state.paths
        ]
        paths.sort()

        table[state.id] = paths
        for _, dst in state.paths:
            if dst.id not in explored:
                explored.add(dst.id)
                frontier.push(dst)
    return table
