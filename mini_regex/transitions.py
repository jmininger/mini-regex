# class Transition:
#     def is_available(self, char):
#         return Exception("Abstract class")

#     def eats_input(self):
#         return Exception("Abstract class")


# class CharLiteralTransition(Transition):
#     def __init__(self, char):
#         self._char = char

#     def is_available(self, char):
#       """ Determines if a character is a member of this particular character
#             class """
#         return self._char == char

#     def eats_input(self):
#         return True


# class EpsilonTransition(Transition):
#     def is_available(self, char):
#         return True

#     def eats_input(self):
#         return False


# class MetaCharTransition(Transition):
#     def is_available(self, char):
#         return char != "\n"

#     def eats_input(self):
#         return True


# class CaseInsensitiveTransition(CharLiteralTransition):
#     def __init__(self, char):
#         super().__init__(char)

#     def is_available(self, char):
#         return self._char.upper() == char.upper()

#     def eats_input(self):
#         return True

class Transition:
    def __init__(self, func, eats_input):
        self._is_available = func
        self._eats_input = eats_input

    def is_available(self, char):
        return self._is_available(char)

    def eats_input(self):
        return self._eats_input


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
            return Transition(f_neg, True)
        else:
            return Transition(f, True)


def create_char_trans(char):
    def f(c):
        return c == char
    return Transition(f, True)


def create_epsilon_trans():
    def f(c):
        return True
    return Transition(f, False)


def create_metachar_trans():
    def f(c):
        return not c == '\n'
    return Transition(f, True)
