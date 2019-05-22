class Transition:
    def __init__(self, func, eats_input, desc):
        self._is_available = func
        self._eats_input = eats_input
        # descriptor for debug
        self._desc = desc

    def __str__(self):
        return self._desc

    def is_available(self, char):
        return self._is_available(char)

    def eats_input(self):
        return self._eats_input


def create_char_trans(char):
    def f(c):
        return c == char
    return Transition(f, True, char)


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

    def add_range(self, ascii_range):
        def f(c):
            (start, end) = ascii_range
            return ord(start) <= ord(c) and ord(c) <= ord(end)
        self.funcs.append(f)

    def add_char(self, char):
        def f(c):
            return c == char
        self.funcs.append(f)

    def create_trans(self):
        def f(char):
            for func in self.funcs:
                if func(char):
                    return True
            return False

        def f_neg(char):
            return not f(char)

        if self.negate:
            return Transition(f_neg, True, "class")
        else:
            return Transition(f, True, "class")
