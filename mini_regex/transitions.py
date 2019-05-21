class Transition:
    def is_available(self, char):
        return Exception("Abstract class")

    def eats_input(self):
        return Exception("Abstract class")


class CharLiteralTransition(Transition):
    def __init__(self, char):
        self._char = char

    def is_available(self, char):
        """ Determines if a character is a member of this particular character
            class """
        return self._char == char

    def eats_input(self):
        return True


class EpsilonTransition(Transition):
    def is_available(self, char):
        return True

    def eats_input(self):
        return False


class MetaCharTransition(Transition):
    def is_available(self, char):
        return char != "\n"

    def eats_input(self):
        return True


class CaseInsensitiveTransition(CharLiteralTransition):
    def __init__(self, char):
        super().__init__(char)

    def is_available(self, char):
        return self._char.upper() == char.upper()

    def eats_input(self):
        return True
