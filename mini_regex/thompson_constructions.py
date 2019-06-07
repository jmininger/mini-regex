from mini_regex.nfa import NFAState, NFA
from mini_regex.transitions import (
    create_epsilon_trans,
)

""" A regular expression can be thought of as an algebra with 3 operators, and
non-deterministic finite automatas as operands. From the three main operations,
(concat, union, kleene's star), all other operations in the parser can be
derived.

For more information, read the
 Dragon Book (Compilers: Principles, Techniques, and Tools), Chapter 3,

 and peep the wikipedia article below:
https://en.wikipedia.org/wiki/Thompson%27s_construction
"""


def construct_graph(transition, id_alloc):
    """ A bi-state automata with a single transtion
    Ex) state1 -> some transition -> state2
    """
    start = NFAState(id_alloc.create_id())
    end = NFAState(id_alloc.create_id())
    start.add_path(transition, end)
    return NFA(start, end)


def concat(graph1, graph2):
    """ Ex) abc -> concat(concat(a, b), c)
    """
    # Optimization: Remove graph2.start by moving all of
    # its paths over to graph2.end
    for path in graph2.start.paths:
        trans, dst_state = path
        graph1.end.add_path(trans, dst_state)
    return NFA(graph1.start, graph2.end)


def union(graph1, graph2, id_alloc):
    """ A union is represented by the pipe operator ('|')
    """
    new_start = NFAState(id_alloc.create_id())
    new_start.add_path(create_epsilon_trans(), graph1.start)
    new_start.add_path(create_epsilon_trans(), graph2.start)
    new_end = NFAState(id_alloc.create_id())
    graph1.end.add_path(create_epsilon_trans(), new_end)
    graph2.end.add_path(create_epsilon_trans(), new_end)
    return NFA(new_start, new_end)


def kstar(graph, id_alloc):
    """ Kleene Star operator """
    new_start = NFAState(id_alloc.create_id())
    new_start.add_path(create_epsilon_trans(), graph.start)
    new_end = NFAState(id_alloc.create_id())
    new_start.add_path(create_epsilon_trans(), new_end)
    graph.end.add_path(create_epsilon_trans(), new_end)
    graph.end.add_path(create_epsilon_trans(), graph.start)
    return NFA(new_start, new_end)


def repeater(graph, repeater_tok, id_alloc):
    """ Constructs an nfa for '*', '+', '?'
    """
    if repeater_tok.has_val('*'):
        return kstar(graph, id_alloc)
    elif repeater_tok.has_val('+'):
        kstar_graph = kstar(graph, id_alloc)
        return concat(graph, kstar_graph)
    elif repeater_tok.has_val('?'):
        empty_graph = construct_graph(create_epsilon_trans(), id_alloc)
        return union(graph, empty_graph)
    else:
        raise Exception("repeater not recognized: " + repeater_tok)
