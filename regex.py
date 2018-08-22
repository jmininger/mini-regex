import unittest as ut


def find_single_match(pattern, search_space):
    # add end char? or do it with the parser?
    try:
        nfa = construct_nfa(pattern)
    except ParsingError as e:
        print('Parsing Error in pattern position: ', e.pos)
    simulator = NfaSimulator(nfa)
    for char in search_space:
        if simulator.has_match():
            return simulator.get_matches()[0]
        else:
            simulator.next_state(char)
    # Do a better job here of figuring out how to return None
    return simulator.get_matches()
    # If no matches, print a message: "No matches"


class TestRegexSearch(ut.TestCase):
    def test_single_search(self):
        test_searches = [
                'hello world my name is jacquin',
                'regex engines are cool',
                'Baz Baz Foo'
            ]
        for sentence in test_searches:
            match = find_single_match('my | oo* | q', search_space=sentence)
            self.assertTrue(match)

    def test_no_match(self):
        test_searches = ['hello', 'no matche']
        for sentence in test_searches:
            match = find_single_match('helloWorld | matches | j', sentence)
            self.assertFalse(match)
