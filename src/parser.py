import unittest as ut
from enum import Enum
from nfa import NFA, NFAState
from stack import Stack
from tokenizer import Tokenizer
from transitions import EpsilonTransition, CharLiteralTransition, \
        MetaCharTransition


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

NodeType = namedtuple('NodeType', ['op', 'graph'])


class Ops(Enum):
    CONCAT = 0
    UNION = 1
    KLEENE = 2
    NOOP = 3
    ERROR = 4


class IDAllocator:
    def __init__(self):
        self._num = -1

    def next(self):
        self._num += 1
        return self._num


# Only eat up a char on a terminal, not on non-terminals


class RegexParser:
    def __init__(self, tokenizer, allocator=IDAllocator()):
        self.tokenizer = tokenizer
        self.id_alloc = allocator

    def construct_nfa(self):
        # Turn start, end tuple into an nfa
        return self.parse_exp()

    def parse_exp(self):
        tok = self.tokenizer.peek()
        if tok.is_char() or tok.is_lparen():
            term = self.parse_term()
            exp2 = self.parse_exp2()
            if exp2.op == Ops.UNION:
                return union(term, exp2.graph, self.id_alloc)
            else:
                return term
            # Return types return both an operator and an automata where both
            # can be None
        else:
            return 'ERROR'

    def parse_exp2(self):
        tok = self.tokenizer.peek()
        if tok.is_union():
            self.tokenizer.next()
            return NodeType(Ops.UNION, self.parse_exp())
        elif tok.is_end() or tok.is_lparen():
            # self.tokenizer.next()
            return NodeType(Ops.NOOP, None)
        else:
            return NodeType(Ops.ERROR, None)

    def parse_term(self):
        tok = self.tokenizer.peek()
        if tok.is_char() or tok.is_lparen():
            factor = self.parse_factor()
            term2 = self.parse_term2()
            if term2.op == Ops.CONCAT:
                return concat(factor, term2.graph)
            else:
                return factor
        else:
            return "HELLPPPP"
        # THROW AN EXCEPTION
            # return NodeType('ERROR', None)

    def parse_term2(self):
        tok = self.tokenizer.peek()
        if tok.is_char() or tok.is_lparen():
            return NodeType(Ops.CONCAT, self.parse_term())
        elif tok.is_rparen() or tok.is_union() or tok.is_end():
            return NodeType(Ops.NOOP, None)
        else:
            return NodeType(Ops.ERROR, None)

    def parse_factor(self):
        tok = self.tokenizer.peek()
        if tok.is_char() or tok.is_lparen():
            char = self.parse_char()
            factor2 = self.parse_factor2()
            if factor2.op == Ops.KLEENE:
                return kstar(char, self.id_alloc)
            else:
                return char
        else:
            return NodeType(Ops.ERROR, None)

    def parse_factor2(self):
        tok = self.tokenizer.peek()
        if tok.is_star():
            self.tokenizer.next()
            return NodeType(Ops.KLEENE, None)
        else:
            return NodeType(Ops.NOOP, None)

    def parse_char(self):
        tok = self.tokenizer.peek()
        if tok.is_char() and tok.is_metachar():
            self.tokenizer.next()
            return construct_graph(MetaCharTransition(), self.id_alloc)
        elif tok.is_char():
            self.tokenizer.next()
            return construct_graph(CharLiteralTransition(tok.val),
                                   self.id_alloc)
        elif tok.is_lparen():
            self.tokenizer.next()
            exp = self.parse_exp()
            tok = self.tokenizer.peek()
            if tok.is_rparen():
                self.tokenizer.next()
                return exp
            else:
                return NodeType(Ops.ERROR, None)
        else:
            return NodeType(Ops.ERROR, None)


def pretty_print_nfa(nfa_start):
    explored = set()
    frontier = Stack()
    table = {}
    frontier.push(nfa_start)
    explored.add(nfa_start.id)

    while not frontier.is_empty():
        state = frontier.top()
        frontier.pop()
        epsilons = [dst.id for trans, dst in state.paths if isinstance(trans,
                    EpsilonTransition)]
        cost_paths = {trans._char: dst.id for trans, dst in state.paths if
                      isinstance(trans, CharLiteralTransition)}

        table[state.id] = cost_paths, epsilons
        for _, dst in state.paths:
            if dst.id not in explored:
                explored.add(dst.id)
                frontier.push(dst)

    return table


class ParserTest(ut.TestCase):
    def test_parse_char(self):
        stream = Tokenizer('a(b|c)')
        parser = RegexParser(stream)
        nfa = parser.parse_exp()
        start, end = nfa
        table = pretty_print_nfa(start)
        print(table)


def concat(graph1, graph2):
    g1_start, g1_end = graph1
    g2_start, g2_end = graph2
    g1_end.add_path(EpsilonTransition(), g2_start)
    return (g1_start, g2_end)


def construct_graph(transition, counter):
    start = NFAState(counter.next())
    end = NFAState(counter.next())
    start.add_path(transition, end)
    return (start, end)


def union(graph1, graph2, counter):
    g1_start, g1_end = graph1
    g2_start, g2_end = graph2
    new_start = NFAState(counter.next())
    new_start.add_path(EpsilonTransition(), g1_start)
    new_start.add_path(EpsilonTransition(), g2_start)
    new_end = NFAState(counter.next())
    g1_end.add_path(EpsilonTransition(), new_end)
    g2_end.add_path(EpsilonTransition(), new_end)
    return (new_start, new_end)


def kstar(graph, counter):
    """ Kleene Star operator """
    g_start, g_end = graph
    new_start = NFAState(counter.next())
    new_start.add_path(EpsilonTransition(), g_start)
    new_end = NFAState(counter.next())
    new_start.add_path(EpsilonTransition(), new_end)
    g_end.add_path(EpsilonTransition(), new_end)
    g_end.add_path(EpsilonTransition(), g_start)
    return (new_start, new_end)


# class TokenType(Enum):
#     Operator = 1
#     Char = 2


'''
E -> T | T+E
T -> int | int+T | (E)

Productions and grammar datastructures should be immutable
Build the tree up and add to an element once you get a connecting point.
Be prepared to remove a node from the tree when it is not

Use recursive calls to emulate a parse tree and to hold the state for it,
but only hold the state in an ast

Ultimately two recursive calls: check if grammar matches and recurse down,
otherwise send no back up
--Recursive call either returns a node that is the root of a syntax tree
(operation?) or None, which implies that the construct does not match

Problem: If the grammar interface is used to recursively check, we can't also
put logic for the operations in there.
Make grammar non-recursive. It either "might match", or doesn't.

GrammarString Match, Production match(tries all grmstring matches)
'''

# test that the parser determines the proper order of things and that it adds
# elements to the stack in the proper fashion. The parser should also be
# responsible for character classes

# test that the builder properly combines nfas. Start testing combos with
# single cell nfas, and then add unit tests to make sure that it merges two
# larger nfas properly.

# An NFABuilder is responsible for combining 2 NFA's using a translation scheme
# based on the operator between them
# All state_ids must be unique


class StreamStub:
    def __init__(self):
        self.iterable = []

    def next(self):
        return next(self.iterable)


if __name__ == '__main__':
    ut.main()
