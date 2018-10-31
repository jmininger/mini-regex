from collections import deque
from nfa import NFAState, NFA
from transitions import CharLiteralTransition, EpsilonTransition


def table_to_nfa(table, start_state, end_state):
    state_table = {id: NFAState(id) for id in table}
    for id, entry in table.items():
        state = state_table[id]
        cost_trans = entry[0]
        epsilon_trans = entry[1]
        for edge, node in cost_trans.items():
            state.add_path(CharLiteralTransition(edge), state_table[node])
        for node in epsilon_trans:
            state.add_path(EpsilonTransition(), state_table[node])
    return NFA(state_table[start_state], state_table[end_state])


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


def nfa_to_table(nfa_start):
    """ Utility function that makes it easier to visualize an nfa and manually
    check its accuracy """
    explored = set()
    frontier = Stack()
    table = {}
    frontier.push(nfa_start)
    explored.add(nfa_start.id)

    while not frontier.is_empty():
        state = frontier.top()
        frontier.pop()
        epsilons = [dst.id for trans, dst in state.paths if isinstance(trans,
                    EpsilonTransition)]
        cost_paths = {trans._char: dst.id for trans, dst in state.paths if
                      isinstance(trans, CharLiteralTransition)}

        table[state.id] = cost_paths, epsilons
        for _, dst in state.paths:
            if dst.id not in explored:
                explored.add(dst.id)
                frontier.push(dst)

    return table


class Option:
    """ An Option type inspired by the type by the same name in OCaml and other
    functional languages. Allows a value to either exist or is None otherwise.
    The use of this type is debatable given python's dynamic types. I've added
    it because I didn't like the idea of returning None in a function that
    might also return a value, and I thought that this might make the code more
    expressive

    Example:
        def foo(num):
            if num % 2 == 0:
                return Option(num)
            else:
                return Option()
        x = foo(5)
        if x.does_contain():
            print(x.get_val())
    """

    def __init__(self, val=None):
        self.val = val
        self.type = True if val else False

    def does_contain(self):
        return self.type

    def get_val(self):
        if self.is_none():
            raise Exception("attempt to access a None value in an Option type")
        else:
            return self.val


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
