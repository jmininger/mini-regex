
class GrammarString:
 	def __init__(self, *args):
 		self._constituents = list(args)

 	def match(tokens):
 		for elem in _constituents:
 			if not elem.match(tokens):
 				return False
 		return True


terminals = ['concat', 'union', 'kleene', 'char']
class Terminal():
	def __init__(self, tok):
		self._val = tok
	
	def match(toks):
		return toks.get() == _val

		#certain terminals need to get functions to call when they are found


class NonTerminal: #Same as a prodcuction, no difference
 	def __init__(self, *gstrings):
 		self._strings = list(gstrings) #grammar strings
 	
 	def match(toks):
 		for elem in _strings:
 			if elem.match(toks):
 				return True
 		return False


e=e1=t=t1=f=f1=c= None
e = NonTerminal(GrammarString(t, e1))
e1 = NonTerminal(GrammarString(Terminal('|'), e), GrammarString(''))
t = NonTerminal(GrammarString(f, t1))
t1 = NonTerminal(GrammarString(t), GrammarString(''))
f = NonTerminal(GrammarString(c, f1))
f1 = NonTerminal(GrammarString(Terminal('*')), GrammarString(''))
c = NonTerminal(GrammarString(Terminal('.')), GrammarString(Terminal('('), e, Terminal(')')))

grammar = e

# grammar = {
# 	'E' : NonTerminal(GrammarString('T', 'E\'')),
# 	'E\'': NonTerminal(GrammarString(Terminal('|'), 'E'), GrammarString('')),
# 	'T' : NonTerminal(GrammarString('F', 'T\'')),
# 	'T\'': NonTerminal(GrammarString('T'), GrammarString('')),
# 	'F' : NonTerminal(GrammarString('C', 'F\'')),
# 	'F\'': NonTerminal(GrammarString(Terminal('*')), GrammarString('')),
# 	'C' : NonTerminal(GrammarString(Terminal('.')), GrammarString(Terminal('('), 'E', Terminal(')')))

# }
print(e)