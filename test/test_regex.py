import mini_regex.regex as RE
import unittest as ut


class RegexEngineTest(ut.TestCase):
    def test_single_char_match(self):
        pattern = "a"
        regex = RE.MiniRegex(pattern)
        search_str = "a"
        self.assertListEqual(regex.find_all_matches(search_str), [(0, 0)])

    def test_single_match(self):
        pattern = ".el*o"
        regex = RE.MiniRegex(pattern)

        search_str = "Hello World!"
        self.assertListEqual(regex.find_all_matches(search_str), [(0, 4)])

        search_str = "Yelllloooooooee"
        self.assertListEqual(regex.find_all_matches(search_str), [(0, 6)])

        search_str = "Not a match"
        self.assertListEqual(regex.find_all_matches(search_str), [])

    def test_is_greedy(self):
        pattern = "a|ab"
        regex = RE.MiniRegex(pattern)
        search_str = "ab"
        self.assertListEqual([(0, 1)], regex.find_all_matches(search_str))

    def test_overlapping_matches(self):
        pattern = "abc|bcde"
        regex = RE.MiniRegex(pattern)
        search_str = "abcde"
        self.assertListEqual(regex.find_all_matches(search_str), [(0, 2)])

    def test_matches_occuring_later(self):
        pattern = "abc|bcde"
        regex = RE.MiniRegex(pattern)
        search_str = "kbcde"
        self.assertListEqual(regex.find_all_matches(search_str), [(1, 4)])

    def test_char_class(self):
        pattern = "[1-9]*"
        regex = RE.MiniRegex(pattern)
        search_str = "123abc456def0"
        self.assertListEqual(regex.find_all_matches(search_str),
                             [(0, 2), (6, 8)])
