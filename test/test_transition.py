import unittest as ut
from mini_regex.transitions import RegexClassBuilder, \
    create_epsilon_trans, create_char_trans, create_metachar_trans


class TransitionTest(ut.TestCase):
    def test_char_literal(self):
        transition = create_char_trans('a')
        self.assertTrue(transition.is_available('a'))
        self.assertFalse(transition.is_available('c'))

    def test_metachar_dot(self):
        transition = create_metachar_trans()
        self.assertTrue(transition.is_available('a'))
        self.assertTrue(transition.is_available('b'))
        self.assertFalse(transition.is_available('\n'))

    # def test_upper_lower_case_meta(self):
    #     transition = CaseInsensitiveTransition('a')
    #     self.assertTrue(transition.is_available('a'))
    #     self.assertTrue(transition.is_available('A'))

    #     self.assertFalse(transition.is_available('b'))
    #     self.assertFalse(transition.is_available('B'))

    # def test_upper_lower_case_works_with_nonalpha_chars(self):
    #     transition = CaseInsensitiveTransition('-')
    #     self.assertTrue(transition.is_available('-'))
    #     self.assertFalse(transition.is_available('a'))

    def test_epsilon_transition_always_passes(self):
        transition = create_epsilon_trans()
        self.assertTrue(transition.is_available('a'))
        self.assertTrue(transition.is_available('A'))
        self.assertTrue(transition.is_available('0'))
        self.assertTrue(transition.is_available('-'))
        self.assertTrue(transition.is_available('\n'))

    def test_class_builder(self):
        class_ = RegexClassBuilder()
        class_.add_char('a')
        class_.add_range(('1', '7'))
        transition = class_.create_trans()
        self.assertTrue(transition.is_available('a'))
        self.assertFalse(transition.is_available('b'))

        self.assertTrue(transition.is_available('1'))
        self.assertTrue(transition.is_available('5'))
        self.assertTrue(transition.is_available('7'))
        self.assertFalse(transition.is_available('0'))


if __name__ == '__main__':
    ut.main()
