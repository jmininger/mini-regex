from util import Stack


class DFASimulator:  # NFARunner?
    def __init__(self, nfa):
        self.nfa = nfa
        self.dfa = [nfa.start]

    def advance_state(self, input):
        explored = set()
        frontier = Stack()
        next_state = []
        for partial_state in self.dfa:
            for node in partial_state.available_paths(input):
                if node.id not in explored:
                    explored.add(node.id)
                    frontier.push(node)
                    next_state.append(node)
        # Now each node has moved once...so the next states and their
        # epsilon closure is the set of all nodes in the next state
        while not frontier.is_empty():
            node = frontier.top()
            frontier.pop()
            free_nodes = node.epsilon_paths()
            for n in free_nodes:
                if n.id not in explored:
                    explored.add(n.id)
                    frontier.push(n)
                    next_state.append(n)
        self.dfa = next_state
        return self.nfa.end.id in explored

    def reset(self):
        self.dfa = [self.nfa.start]

    def is_active(self):
        return len(self.dfa) != 0
