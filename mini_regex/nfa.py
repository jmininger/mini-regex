class NFA:
    """ A labeled tuple
    The end state is only reachable from the start state via references/python
    pointers. This makes it harder to traverse the graph in an improper manner
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end


class NFAState:
    """ A state is nothing more than an ID and a list of
    transition -> destination_id tuples
    """

    def __init__(self, id):
        self.id = id
        self.paths = set()

    def __str__(self):
        header = "NFAState: " + str(self.id)
        paths = [str(dst.id) for _, dst in self.paths]
        paths.sort()
        return header + " Paths: " + ", ".join(paths) + "||"

    def __repr__(self):
        return str(self.id) + " " + str(self.paths)

    def add_path(self, transition, destination):
        path = (transition, destination)
        self.paths.add(path)

    def available_cost_paths(self, char):
        """ Returns all available paths that require a character as input (that
        "cost") and that match the input char
        """
        return set([
            destination
            for transition, destination in self.paths
            if transition.eats_input() and transition.is_available(char)
        ])

    def epsilon_paths(self):
        return set([
            destination
            for transition, destination in self.paths
            if not transition.eats_input()
        ])
