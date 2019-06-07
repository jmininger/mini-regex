class Transition:
    def __init__(self, func, eats_input, desc):
        self._is_available = func
        self._eats_input = eats_input
        self._desc = desc  # descriptor for debugs and error msgs

    def __str__(self):
        return self._desc

    def __eq__(self, other):
        return self._desc == other._desc

    def __hash__(self):
        return hash(self._desc)

    def is_available(self, char):
        """ Given the next char, tell if this transition is available as a path
        to another state.
        """
        return self._is_available(char)

    def eats_input(self):
        return self._eats_input


"""
    Transitions:
        Take an "acceptance" function that takes a char and returns a boolean
        if the state is allowed to advance on the transition.
"""


def create_char_trans(char):
    def f(c):
        return c == char
    return Transition(f, True, ("char: " + char))


def create_epsilon_trans():
    def f(c):
        return True
    return Transition(f, False, "epsilon")


def create_metachar_trans():
    def f(c):
        return not c == '\n'
    return Transition(f, True, "metachar")


class RegexClassBuilder:
    def __init__(self, negate=False):
        self.funcs = []
        self.negate = negate
        self.desc = []

    def add_range(self, ascii_range):
        (start, end) = ascii_range

        def f(c):
            return ord(start) <= ord(c) and ord(c) <= ord(end)
        self.funcs.append(f)
        self.desc.append(start + "-" + end)

    def add_char(self, char):
        def f(c):
            return c == char
        self.funcs.append(f)
        self.desc.append(char)

    def create_trans(self):
        def f(char):
            for func in self.funcs:
                if func(char):
                    return True
            return False

        def f_neg(char):
            return not f(char)

        desc = ''.join([str(x) for x in self.desc])
        if self.negate:
            return Transition(f_neg, True, "neg-class: " + desc)
        else:
            return Transition(f, True, "class: " + desc)
