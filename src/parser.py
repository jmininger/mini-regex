import unittest as ut
from nfa import NFAState, NFA
# from tokenizer import Tokenizer
from transitions import EpsilonTransition, CharLiteralTransition, \
        MetaCharTransition
# from util import table_to_nfa, nfa_to_table

"""
Small recursive descent parser for regex

IN: tokens, OUT: Non-deterministic finite state machine

CFG for regular expressions:
E -> TE`
E`-> '|'E | e
T -> FT`
T`-> T | e
F -> CF`
F`-> '*' | e
C -> char | ( E )
"""


class IDAllocator:

    """ Responsible for providing each state with a unique_id. Not all states
    are initialized at the same time, or even in the same scope, so it makes
    sense to have an allocator that keeps track of which numbers have been used
    """

    def __init__(self):
        # Start at -1 so the first number produced is 0
        self._num = -1

    def create_id(self):
        self._num += 1
        return self._num


def construct_graph(transition, id_alloc):
    start = NFAState(id_alloc.create_id())
    end = NFAState(id_alloc.create_id())
    start.add_path(transition, end)
    return (start, end)


def concat(graph1, graph2):
    g1_start, g1_end = graph1
    g2_start, g2_end = graph2
    g1_end.add_path(EpsilonTransition(), g2_start)
    return (g1_start, g2_end)


def union(graph1, graph2, id_alloc):
    g1_start, g1_end = graph1
    g2_start, g2_end = graph2
    new_start = NFAState(id_alloc.create_id())
    new_start.add_path(EpsilonTransition(), g1_start)
    new_start.add_path(EpsilonTransition(), g2_start)
    new_end = NFAState(id_alloc.create_id())
    g1_end.add_path(EpsilonTransition(), new_end)
    g2_end.add_path(EpsilonTransition(), new_end)
    return (new_start, new_end)


def kstar(graph, id_alloc):
    """ Kleene Star operator """
    g_start, g_end = graph
    new_start = NFAState(id_alloc.create_id())
    new_start.add_path(EpsilonTransition(), g_start)
    new_end = NFAState(id_alloc.create_id())
    new_start.add_path(EpsilonTransition(), new_end)
    g_end.add_path(EpsilonTransition(), new_end)
    g_end.add_path(EpsilonTransition(), g_start)
    return (new_start, new_end)


class RegexParser:
    def __init__(self, tokenizer, allocator=IDAllocator()):
        self.tokenizer = tokenizer
        self.id_alloc = allocator

    def construct_nfa(self):
        # Turn start, end tuple into an nfa
        return NFA(*self.parse_exp())

    def parse_exp(self):
        tok = self.tokenizer.peek()
        if tok.is_char() or tok.is_lparen():
            term = self.parse_term()
            exp2 = self.parse_exp2()
            if exp2:
                return union(term, exp2, self.id_alloc)
            else:
                return term
        else:
            raise Exception("unexpected token in parse_exp at pos: " +
                            str(tok.pos))

    def parse_exp2(self):
        tok = self.tokenizer.peek()
        if tok.is_union():
            self.tokenizer.next()
            return self.parse_exp()
        elif tok.is_end() or tok.is_rparen():
            # self.tokenizer.next()
            return None
        else:
            raise Exception("unexpected token in parse_exp2 at pos: " +
                            str(tok.pos))

    def parse_term(self):
        tok = self.tokenizer.peek()
        if tok.is_char() or tok.is_lparen():
            factor = self.parse_factor()
            term2 = self.parse_term2()
            if term2:
                return concat(factor, term2)
            else:
                return factor
        else:
            raise Exception("unexpected token in parse_term at pos: " +
                            str(tok.pos))

    def parse_term2(self):
        tok = self.tokenizer.peek()
        if tok.is_char() or tok.is_lparen():
            return self.parse_term()
        elif tok.is_rparen() or tok.is_union() or tok.is_end():
            return None
        else:
            raise Exception("unexpected token in parse_term2 at pos: " +
                            str(tok.pos))

    def parse_factor(self):
        tok = self.tokenizer.peek()
        if tok.is_char() or tok.is_lparen():
            char = self.parse_char()
            factor2 = self.parse_factor2()
            if factor2:
                return kstar(char, self.id_alloc)
            else:
                return char
        else:
            raise Exception("unexpected token in parse_factor at pos: " +
                            str(tok.pos))

    def parse_factor2(self):
        tok = self.tokenizer.peek()
        if tok.is_star():
            self.tokenizer.next()
            return True
        else:
            return None

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
                raise Exception("unexpected token in parse_char at pos: " +
                                str(tok.pos))
        else:
            raise Exception("unexpected token in parse_char at pos: " +
                            str(tok.pos))


if __name__ == '__main__':
    ut.main()
