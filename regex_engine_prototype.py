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
# states = []
# def getNewID():
#     return len(states)

# class State:
#     def __init__(self):
#         self._id = getNewID()
#         states.append(self)
#         self._transitions = {}
#         self._epsilons = []
#         self._is_end = False
    
#     def addTransition(char, next_state):
#         _transitions[char] = next_state
    
#     def addEpsilon(next_state):
#         _epsilons.append(next_state)

#     def getNextState(char):
#         return _transitions[char]

class Automata:
    def match(str):   
        pass
    
    def matchFirst(str):
        pass

    # def __init__(self, initial = None):
    #     self._start = State()
    #     self._finish = State()
    #     _finish._is_end = True
    #     if initial:
    #         _start.addTransition(initial, _finish)
    #     else:
    #         _start.addEpsilon(_finish)


# class AutomataFactory: 
#     def concatTransition(nfa):
#         for tran, state in nfa._start._transitions:
#             self._finish.addTransition(tran, state)
#         for e in nfa._start._epsilons:
#             self._finish.addEpsilon(e)
#         self._finish = nfa._finish

        
#     transitions = {
#         "concat": concatTransition,
#         "union":  unionTransition,
#         "kleene": kleeneTransition
#     }

#     def __init__(self):
#         self._start = State()
#         _start.addEpsilon(_finish)
#         self._finish = State()
#         _start.addEpsilon(_finish)
#         self._current = _start
    
#     def addTransition(enum, elem):
#         transitions[enum](elem)


# class TestAutomataMethods(unittest.TestCase):
#     def test_concatenation(self):
#         af = AutomataFactory()
#         af.addTransition('concat', 'a')
#         af.addTransition('concat', 'b')
#         nfa = af.create()
#         self.assertTrue(nfa.run('acbabde'))

        #self.assertEquals(y.x, 1)

def regex_compile(regex):
    return Automata()

class TestRegexDriver(unittest.TestCase):
    def test_compile_method(self):
        automata = regex_compile('ab|c*')
        self.assertTrue(isinstance(automata, Automata))

    def test_regex_matcher(self):
        regex = regex_compile('hello|world')
        inputStr = 'hello world my name is Jacq'
        self.assertEquals(regex.matchFirst(inputStr), 0)




class Production:
    def __init__(self):
        pass
class GrammarConstruct:
    def __init__(self):
        pass
class Terminal(GrammarConstruct):
    pass
class NonTerminal(GrammarConstruct): 
    pass
class AST:
    pass

if __name__ == '__main__':
    unittest.main()