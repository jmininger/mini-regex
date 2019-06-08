import mini_regex.regex as RE
import unittest as ut


class RegexEngineTest(ut.TestCase):
    def test_single_char_match(self):
        pattern = "a"
        regex = RE.MiniRegex(pattern)
        search_str = "a"
        match = regex.find_match_at(search_str)
        self.assertEqual(match.get_span(), (0, 0))

    def test_single_match(self):
        pattern = ".el+o"
        regex = RE.MiniRegex(pattern)

        search_str = "Hello World!"
        matches = regex.find_all_matches(search_str)
        result = [match.get_span() for match in matches]
        self.assertListEqual(result, [(0, 4)])

        search_str = "Yelllloooooooee"
        matches = regex.find_all_matches(search_str)
        result = [match.get_span() for match in matches]
        self.assertListEqual(result, [(0, 6)])

        search_str = "Not a match"
        matches = regex.find_all_matches(search_str)
        result = [match.get_span() for match in matches]
        self.assertListEqual(result, [])

    def test_is_greedy(self):
        pattern = "a|ab"
        regex = RE.MiniRegex(pattern)
        search_str = "ab"
        matches = regex.find_all_matches(search_str)
        result = [match.get_span() for match in matches]
        self.assertListEqual(result, [(0, 1)])

    def test_overlapping_matches(self):
        pattern = "abc|bcde"
        regex = RE.MiniRegex(pattern)
        search_str = "abcde"
        matches = regex.find_all_matches(search_str)
        result = [match.get_span() for match in matches]
        self.assertListEqual(result, [(0, 2)])

    def test_matches_occuring_later(self):
        pattern = "abc|bcde"
        regex = RE.MiniRegex(pattern)
        search_str = "kbcde"
        matches = regex.find_all_matches(search_str)
        result = [match.get_span() for match in matches]
        self.assertListEqual(result, [(1, 4)])


    def test_char_class(self):
        pattern = "[1-9]+"
        regex = RE.MiniRegex(pattern)
        search_str = "123abc456def0"
        matches = regex.find_all_matches(search_str)
        result = [match.get_span() for match in matches]
        self.assertListEqual(result, [(0, 2), (6, 8)])
