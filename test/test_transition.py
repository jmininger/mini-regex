import unittest as ut
from mini_regex.transitions import CharLiteralTransition, MetaCharTransition, \
                        CaseInsensitiveTransition, EpsilonTransition


class TransitionTest(ut.TestCase):
    def test_char_literal(self):
        transition = CharLiteralTransition('a')
        self.assertTrue(transition.is_available('a'))
        self.assertFalse(transition.is_available('c'))

    def test_metachar_dot(self):
        transition = MetaCharTransition()
        self.assertTrue(transition.is_available('a'))
        self.assertTrue(transition.is_available('b'))
        self.assertFalse(transition.is_available('\n'))

    def test_upper_lower_case_meta(self):
        transition = CaseInsensitiveTransition('a')
        self.assertTrue(transition.is_available('a'))
        self.assertTrue(transition.is_available('A'))

        self.assertFalse(transition.is_available('b'))
        self.assertFalse(transition.is_available('B'))

    def test_upper_lower_case_works_with_nonalpha_chars(self):
        transition = CaseInsensitiveTransition('-')
        self.assertTrue(transition.is_available('-'))
        self.assertFalse(transition.is_available('a'))

    def test_epsilon_transition_always_passes(self):
        transition = EpsilonTransition()
        self.assertTrue(transition.is_available('a'))
        self.assertTrue(transition.is_available('A'))
        self.assertTrue(transition.is_available('0'))
        self.assertTrue(transition.is_available('-'))
        self.assertTrue(transition.is_available('\n'))


if __name__ == '__main__':
    ut.main()
