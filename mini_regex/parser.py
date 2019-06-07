from mini_regex.transitions import (
    RegexClassBuilder,
    create_char_trans,
    create_metachar_trans,
)

from mini_regex.thompson_constructions import (
    construct_graph,
    concat,
    union,
    repeater
)


"""
Small recursive descent parser for regex

IN: tokens, OUT: Non-deterministic finite state machine

CFG for regular expressions:
Exp -> Term Exp`
Exp`-> '|'Exp | empty
Term -> Factor Term`
Term`-> Term | empty
Factor -> C Factor`
Factor`-> '*'|'?'|'+'| empty
C -> CharType | ( Exp )
CharType -> Class | Char | MetaChar
Char -> All ascii chars not including metachars or metachars with front slash
MetaChars -> . | \\b | '|' | * | ? | + | ( | ) | [ | ]
Class -> '[' InnerClass ']' | '[^' InnerClass ']'
InnerClass -> Range | ClassChars
Range -> ClassChars - ClassChars
ClassChars -> Ascii chars, no special chars
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


# def construct_graph(transition, id_alloc):
#     start = NFAState(id_alloc.create_id())
#     end = NFAState(id_alloc.create_id())
#     start.add_path(transition, end)
#     return NFA(start, end)


# def concat(graph1, graph2):
#     # Remove graph2.start by moving all of its paths over to graph2.end
#     for path in graph2.start.paths:
#         trans, dst_state = path
#         graph1.end.add_path(trans, dst_state)
#     return NFA(graph1.start, graph2.end)


# def union(graph1, graph2, id_alloc):
#     new_start = NFAState(id_alloc.create_id())
#     new_start.add_path(create_epsilon_trans(), graph1.start)
#     new_start.add_path(create_epsilon_trans(), graph2.start)
#     new_end = NFAState(id_alloc.create_id())
#     graph1.end.add_path(create_epsilon_trans(), new_end)
#     graph2.end.add_path(create_epsilon_trans(), new_end)
#     return NFA(new_start, new_end)


# def kstar(graph, id_alloc):
#     """ Kleene Star operator """
#     new_start = NFAState(id_alloc.create_id())
#     new_start.add_path(create_epsilon_trans(), graph.start)
#     new_end = NFAState(id_alloc.create_id())
#     new_start.add_path(create_epsilon_trans(), new_end)
#     graph.end.add_path(create_epsilon_trans(), new_end)
#     graph.end.add_path(create_epsilon_trans(), graph.start)
#     return NFA(new_start, new_end)


# def repeater(graph, repeater_tok, id_alloc):
#     if repeater_tok.has_val('*'):
#         return kstar(graph, id_alloc)
#     elif repeater_tok.has_val('+'):
#         kstar_graph = kstar(graph, id_alloc)
#         return concat(graph, kstar_graph)
#     elif repeater_tok.has_val('?'):
#         empty_graph = construct_graph(create_epsilon_trans(), id_alloc)
#         return union(graph, empty_graph)
#     else:
#         raise Exception("repeater not recognized: " + repeater_tok)


class RegexParser:
    special_chars = [
            "|", "*", "(", ")", ".", "+", "[", "]", "?", "^", "$"
            ]

    def __init__(self, tokenizer):
        self.tok_stream = tokenizer
        self.id_alloc = IDAllocator()
        self.groups = []

    def is_special_token(self, token):
        for char in self.special_chars:
            if token.has_val(char):
                return True
        return False

    def is_literal_token(self, token):
        return not (self.is_special_token(token) or token.is_end())

    def is_meta_token(self, token):
        return token.has_val(".")

    def is_start_of_char(self, tok):
        return (self.is_meta_token(tok) or
                tok.has_val("[") or
                self.is_literal_token(tok))

    def construct_nfa(self):
        return self.parse_exp()

    def parse_exp(self):
        tok = self.tok_stream.peek()

        if self.is_start_of_char(tok) or tok.has_val('('):
            term = self.parse_term()
            exp2 = self.parse_exp2()
            if exp2:
                return union(term, exp2, self.id_alloc)
            else:
                return term
        else:
            raise Exception(
                    "unexpected token in parse_exp at pos: " + str(tok.pos))

    def parse_exp2(self):
        tok = self.tok_stream.peek()
        if tok.has_val('|'):
            self.tok_stream.advance()
            return self.parse_exp()
        elif tok.is_end() or tok.has_val(')'):
            return None
        else:
            raise Exception(
                    "unexpected token in parse_exp2 at pos: " + str(tok.pos))

    def parse_term(self):
        tok = self.tok_stream.peek()

        if self.is_start_of_char(tok) or tok.has_val('('):
            factor = self.parse_factor()
            term2 = self.parse_term2()
            if term2:
                return concat(factor, term2)
            else:
                return factor
        else:
            raise Exception(
                "unexpected token in parse_term at pos: " + str(tok.pos)
            )

    def parse_term2(self):
        tok = self.tok_stream.peek()

        if self.is_start_of_char(tok) or tok.has_val('('):
            return self.parse_term()
        elif tok.has_val(')') or tok.has_val('|') or tok.is_end():
            return None
        else:
            raise Exception(
                "unexpected token in parse_term2 at pos: " + str(tok.pos)
            )

    def parse_factor(self):
        tok = self.tok_stream.peek()

        if self.is_start_of_char(tok) or tok.has_val('('):
            char = self.parse_char()

            tok = self.tok_stream.peek()
            factor2 = self.parse_factor2()
            if factor2:
                return repeater(char, tok, self.id_alloc)
            else:
                return char
        else:
            raise Exception(
                "unexpected token in parse_factor at pos: " + str(tok.pos)
            )

    def parse_factor2(self):
        tok = self.tok_stream.peek()
        if tok.has_val('*') or tok.has_val('+') or tok.has_val('?'):
            self.tok_stream.advance()
            return True
        else:
            return None

    def parse_regex_class(self):
        """ Parses a class.
        Regex classes represent a singular character and are contained within
        "[" and  "]"
        """
        self.tok_stream.advance()  # advance past '['
        tok = self.tok_stream.peek()

        negate_flag = False
        if tok.has_val('^'):
            negate_flag = True
            self.tok_stream.advance()
            tok = self.tok_stream.peek()
        builder = RegexClassBuilder(negate_flag)

        prev_tok = None
        range_start = None
        while not tok.has_val(']'):
            # Add a range
            if prev_tok and tok.has_val('-'):
                range_start = prev_tok
                prev_tok = tok
            elif prev_tok and prev_tok.has_val('-'):
                builder.add_range((range_start.val, tok.val))
                prev_tok = None
                range_start = None
            elif prev_tok:
                builder.add_char(prev_tok.val)
                prev_tok = tok
            else:
                prev_tok = tok
            self.tok_stream.advance()
            tok = self.tok_stream.peek()
        if prev_tok:
            builder.add_char(prev_tok.val)

        self.tok_stream.advance()
        return construct_graph(builder.create_trans(), self.id_alloc)

    def parse_char(self):
        """ Turn a character into an automata.
         A char is a anything represented by a two-state automata with a
         singular transition that eats a char
        """
        tok = self.tok_stream.peek()

        # regex class
        if tok.has_val('['):
            return self.parse_regex_class()

        # metachar
        elif tok.has_val('.'):
            self.tok_stream.advance()
            return construct_graph(create_metachar_trans(), self.id_alloc)

        # char literal
        elif self.is_literal_token(tok):
            self.tok_stream.advance()
            return construct_graph(
                create_char_trans(tok.val), self.id_alloc
            )

        # group start - currently has no effect
        elif tok.has_val('('):
            self.tok_stream.advance()
            exp = self.parse_exp()
            tok = self.tok_stream.peek()
            if tok.has_val(')'):
                self.tok_stream.advance()
                return exp
            else:
                raise Exception(
                    "unexpected token in parse_char at pos: " + str(tok.pos)
                )
        else:
            raise Exception(
                "unexpected token in parse_char at pos: " + str(tok.pos)
            )
