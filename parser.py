'''
Small recursive descent parser for regex

IN: tokens, OUT: AST

CFG for regular expressions:
E -> TE`
E`-> '|'E | e
T -> FT`
T`-> T | e
F -> CF`
F`-> '*' | e
C -> char | ( E )


Grammar can be used as a tree like structure:
AST should only have op and operands and a tree like structure...operands
should be values...nothing else in the tree is neccessary
'''

from collections import namedtuple

NodeType = namedtuple('NodeType', ['op', 'val'])


def ParseExp(stream):
    tok = stream.next()
    if tok == 'CHAR' or tok == 'LPAREN':
        t = ParseTerm(stream)
        e = ParseExp2(stream)
        # if e = command or + automata, evaluate t or e
        # else return t
        # Return types return both an operator and an automata where both can
        # be None
    else:
        return 'ERROR'


def ParseExp2(stream):
    tok = stream.next()
    if tok == 'OR':
        return NodeType('OR', parseExp(stream))
    elif tok == 'END' or tok == 'LPAREN':
        return NodeType('NONE', None)
    else:
        return NodeType('ERROR', None)


def ParseTerm(stream):
    tok = stream.next()
    if tok == 'CHAR' or tok == 'LPAREN':
        f = parseFactor(stream)
        t2 = parseTerm2(stream)
        return ANDCtor(f, t2)
    else:
        return NodeType('ERROR', None)


def ParseTerm2(stream):
    tok = stream.next()
    if tok in ['CHAR', 'LPAREN']:
        pass
    elif tok in ['RPAREN', 'OR', 'END']:
        return NodeType('NONE', None)
    else:
        return NodeType('ERROR', None)


def ParseFactor(stream):
    tok = stream.next()
    if tok == 'CHAR' or tok == 'LPAREN':
        c = parseChar(stream)
        f2 = parseFactor2(stream)
        return KleeneOp(c)
    else:
        return NodeType('ERROR', None)


def ParseFactor2(stream):
    tok = stream.next()
    if tok == 'STAR':
        return NodeType('STAR', None)
    else:
        return NodeType('NONE', None)


def ParseChar(stream):
    tok = stream.next()
    if tok == 'CHAR':
        return Automata(tok.getVal())
    elif tok == 'LPAREN':
        e = parseExp(stream)
        tok = stream.getNext()
        if tok == 'RPAREN':
            return e
        else:
            return NodeType('ERROR', None)
    else:
        return NodeType('ERROR', None)



from abc import ABCMeta

from enum import Enum
import unittest as ut

class TokenType(Enum):
	Operator = 1
	Char = 2



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
