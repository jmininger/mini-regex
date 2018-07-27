'''
	Small recursive descent parser for regex

	IN: tokens, OUT: AST

	ab = 	&
		  |   |
		  a   b


CFG for regular expressions:
	E -> TE`
	E`-> '|'E | e
	T -> FT`
	T`-> T | e
	F -> CF`
	F`-> '*' | e
	C -> char


Grammar can be used as a tree like structure: 
AST should only have op and operands and a tree like structure...operands should be values...nothing else in the tree is neccessary
'''
from abc import ABCMeta

import unittest as ut

class Token:
	def __init__(self, val):
		self._val = val
	# how to define an isEquals func that works for "is/not" builtins?


 class GrammarString:
 	def __init__(self):
 		self._constituents = []

 	def match(tokens):
 		for elem in _constituents:
 			if not elem.match(tokens)
 				return False
 		return True

class Terminal(GrammarElement):
	def __init__(self, tok):
		self._val = tok
	
	def match(toks):
		return toks.get() == _val

		#certain terminals need to get functions to call when they are found


 class NonTerminal(GrammarElement): #Same as a prodcuction, no difference
 	def __init__(self):
 		self._strings = [] #grammar strings
 	
 	def match(toks):
 		for elem in _strings:
 			if elem.match(toks)
 				return True
 		return False


#instead of returning booleans, return an ast
class ASTNode:
	def __init__(self):
		self._children = []
		self._value = Token()


'''
	E -> T | T+E
	T -> int | int+T | (E)

	bool CheckPn()
	bool CheckP()

	Construct.check -> calls other constructs in it and checks recursively
'''
def CheckProduction(prod, tok_stream, ptree):
	for i in prod.constructs:
		return check_i()
def CheckGrammarString(gstring, tok_stream, ptree) 
	for i in gstring:
		if(i.match(t_stream)):
			i.action()
			return True
	return False

def Parse(pattern):
	for p in Grammar.start._productions:
		testP
	return AST()

 '''
 	Productions and grammar datastructures should be immutable
 	Build the tree up and add to an element once you get a connecting point. Be prepared
 		to remove a node from the tree when it is not 

 		Use recursive calls to emulate a parse tree and to hold the state for it,
 		but only hold the state in an ast

 		Grammar is graph based--grammar nodes request a lexer peek(x) if first element is a  

 		Ultimately two recursive calls: check if grammar matches and recurse down, otherwise send no back up
 		--Recursive call either returns a node that is the root of a syntax tree (operation?) or None, which
 		implies that the construct does not match

 		Problem: If the grammar interface is used to recursively check, we can't also put logic for the 
 		operations in there. 
 		Make grammar non-recursive. It either "might match", or doesn't. 

 		GrammarString Match, Production match(tries all grmstring matches)
 '''







class TestParser(ut.TestCase):
	def testTest(self):
		self.assertTrue(5)


if __name__ == '__main__':
	ut.main()
