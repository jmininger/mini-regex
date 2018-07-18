import unittest

''' 
    NEED AN EPSILON TRANSITION

    Composite Pattern: Automata vs State
    Automata and State both have a begin and end, and then have transitions?
    You can feed both of them a single 
    BOTH NEED:
        Matches (stream)/run(stream)

'''
# def regex(pattern, input):
# regex = regex_compile(pattern)
class State:
    def __init__(self):
        self._transitions = {}
        self._epsilons = []
    
    def addTransition(char, next_state):
        _transitions[char] = next_state
    
    def addEpsilon(next_state):
        _epsilons.append(next_state)

    def getNextState(char):
        return _transitions[char]

class Automata:
    def __init__(self, state):
        self._start = State()

class AutomataFactory: 
    transitions = {
        "concat": concatTransition,
        "union":  unionTransition,
        "kleene": kleeneTransition
    }
    def concatTransition(elem):
        elem

    def __init__(self):
        self._start = State()
        _start.addEpsilon(_finish)
        self._finish = State()
        _start.addEpsilon(_finish)
        self._current = _start
    
    def addTransition(enum, elem):
        transitions[enum](elem)


class TestAutomataMethods(unittest.TestCase):
    def test_concatenation(self):
        af = AutomataFactory()
        af.addTransition('concat', 'a')
        af.addTransition('concat', 'b')
        nfa = af.create()
        self.assertTrue(nfa.run('acbabde'))

        #self.assertEquals(y.x, 1)

if __name__ == '__main__':
    unittest.main()