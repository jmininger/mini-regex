class Transition:
    def is_available(self, char):
        return Exception('Abstract class')


class CharLiteralTransition(Transition):
    def __init__(self, char):
        self._char = char

    def is_available(self, char):
        """ Determines if a character is a member of this particular character
            class """
        return self._char == char


class EpsilonTransition(Transition):
    def is_available(self, char):
        return True


class MetaTransition(Transition):
    def is_available(self, char):
        return char != '\n'


class CaseInsensitiveTransition(CharLiteralTransition):
    def __init__(self, char):
        super().__init__(char)

    def is_available(self, char):
        return self._char.upper() == char.upper()
