class NonTerminal:
    def __init__(self, symbol):
        self._symbol = symbol


class Production:
    def __init__(self, lhs, rhs):
	#rhs is a list (tuple) of NTs and Tokens
	self._lhs = lhs
	self._rhs = rhs


class Grammar:
	def __init__(self):
		self._start = NonTerminal()
		pass

	def GetProductions(non_terminal):
		return [for p in _productions, ]
# e = e1 = t = t1 = f = f1 = c = None
# e = NonTerminal(GrammarString(t, e1))
# e1 = NonTerminal(GrammarString(Terminal('|'), e), GrammarString(''))
# t = NonTerminal(GrammarString(f, t1))
# t1 = NonTerminal(GrammarString(t), GrammarString(''))
# f = NonTerminal(GrammarString(c, f1))
# f1 = NonTerminal(GrammarString(Terminal('*')), GrammarString(''))
# c = NonTerminal(GrammarString(Terminal('.')), GrammarString(Terminal('('), e, Terminal(')')))

# grammar = e
def Expression():
	return Term() && ExpPrime()

# grammar = {
# 	'E' : ["T E\'"],
# 	'E\'': [" | E", ""],
# 	'T' : ["F T\'"],
# 	'T\'': [" T ", ""],
# 	'F' : ["C F\'"]
# 	'F\'': ["*", ""],
# 	'C' : [".", "( E )"]
# }
#print(e)
