from mini_regex.util import Stack
from mini_regex.dfa_state import NFAIterator, DFAState


class DFASimulatorBase:
    def __init__(self, nfa):
        # Constant fields
        self.nfa = nfa
        # Mutable fields
        self.dfa = DFAState()

    def get_epsilon_closure(self, dfa_state):
        """ The epsilon closure of a substate is the state containing all
        reachable substates that are accessible without "eating" a character.
        These paths are called "epsilons".
        This function takes a dfa, and adds to it, all substates reachable via
        epsilon paths.

        It is non-mutating, so it returns a new dfa state
        instead of mutating the current one

        IMPORTANT: A DFAState that has not advanced via all possible
        epsilon paths is NOT A VALID DFAState
        """
        # DepthFirstSearch setup

        # prevent cycles
        explored = set()

        # new_dfa_state will only represent the full state at the end of this
        # function call
        new_dfa_state = DFAState()

        substates = dfa_state.get_substates()

        # frontier contains all current substates
        frontier = Stack(substates)

        while not frontier.is_empty():
            substate = frontier.top()
            frontier.pop()

            node = substate.get_node()
            if node not in explored:
                new_dfa_state.add_substate(substate)
                free_nodes = node.epsilon_paths()
                # derive all freely reachable nodes and give them the same age
                new_substates = [NFAIterator(freenode, substate.get_age())
                                 for freenode in free_nodes]
                for new_sub in new_substates:
                    frontier.push(new_sub)
                explored.add(node)
        return new_dfa_state

    def consume_character(self, char, current_dfa):
        """ returns a new_dfa
        """
        new_dfa_state = DFAState()
        substates = current_dfa.get_substates()
        for substate in substates:
            node = substate.node
            for destination in node.available_cost_paths(char):
                # Consumes a char, age increases by one
                new_age = substate.age + 1
                new_substate = NFAIterator(destination, new_age)
                new_dfa_state.add_substate(new_substate)

        # take the new_dfa_state and add the epsilon closure to it
        return self.get_epsilon_closure(new_dfa_state)

    def check_match(self):
        match = self.dfa.get_substate_with_node(self.nfa.end)
        if match:
            return match.get_age()
        else:
            return None

    def check_finished(self):
        return len(self.dfa.get_substates()) == 0


class DFASimulator(DFASimulatorBase):
    def __init__(self, nfa):
        DFASimulatorBase.__init__(self, nfa)

        start_dfa = self.dfa
        start_state = NFAIterator(self.nfa.start, 0)
        start_dfa.add_substate(start_state)
        self.dfa = self.get_epsilon_closure(start_dfa)

    def advance_state(self, char):
        self.dfa = self.consume_character(char, self.dfa)

    def run_sim(self, search_str):
        """ Returns (None | Num chars consumed of the matching iterator)
        Only checks for matching substrings starting at the beginning of
        the search_str paramater
        """
        # Advance via the epsilon closure from the start state. The age is
        # still 0, as no chars have been consumed
        match = self.check_match()
        is_finished = self.check_finished()
        if match:
            return 0
        elif is_finished:
            return None
        else:
            # Main search loop, begin consuming chars
            for c in search_str:
                self.advance_state(c)
                match = self.check_match()
                if match:
                    return match
                if self.check_finished():
                    return None
            return None


# TODO: Below lies an optimized version of a simulation that takes an entire
# search string and finds all matches. It handles greediness and overloading.
# It is extremely ugly, and is in severe need of refactoring. It also relies on
# a number of apis that have since changed.

# class MultiDFASimulator(DFASimulatorBase):  # NFARunner?
#     """This class should only be used when you want to search an entire string
#     for all possible matches. It is much more optimized than DFASim
#     A search string of size n contains n different substrings which need to
#     be fed into the automata to check for a match. Instead of running each
#     automata seperately (an O(n^2) runttime), this algorithm does not backtrack
#     and keeps track of each of these automatas simultaneously, only running a
#     single loop (O(n)) through the search space.
#     """
#     def __init__(self, nfa):
#         DFASimulatorBase.__init__(self, nfa)

#         # iterators with ages in this set are invalid
#         self.age_restrictions = set()

#     def _build_start_iters(self):
#         explored = set()
#         frontier = Stack()
#         closure = []
#         # dst = destination
#         for dst in self.nfa.start.epsilon_paths():
#             if dst.id not in explored:
#                 explored.add(dst.id)
#                 frontier.push(dst)
#         while not frontier.is_empty():
#             dst = frontier.top()
#             frontier.pop()
#             closure.append(NFAIterator(dst, self.current_age))
#         return closure

#     def _merge_start_dfa(self):
#         """ Each cycle (a single input char from a search string) starts its
#         own...needed b/c there may be epsilon closures in the start state. The
#         graph must move forward at all times when possible, and at the start
#         state, these epsilons need to be advanced
#         """
#         for iter in self._build_start_iters():
#             self.dfa.add_iterator(iter)
#         self.dfa.add_iterator(NFAIterator(self.nfa.start, self.current_age))

#     # def reset_state(self):
#     #     self.current_age = -1
#     #     self.dfa = DFAState()
#     #     self.age_restrictions = set()

#     def advance_state(self, char):
#         pass

#     def advance_multi_state(self, search_str):
#         start_dfa = self.dfa
#         start_state = NFAIterator(self.nfa.start, 0)
#         start_dfa.add_substate(start_state)


#         self.dfa = self.get_epsilon_closure(self.dfa)

#         explored = set()
#         # Given the current state, each state_iter spawns new state_iters, that
#         # have eaten the current input and can be put in the next_state
#         next_state = DFAState()
#         match = None

#         self._merge_start_dfa()
#         for iter in self.dfa.get_iterators():
#             # If a match ending with the current char has been found, and if
#             # all iterators of the same age have been updated, return the match
#             if match and iter.age > match[0]:
#                 self.dfa = next_state
#                 return match

#             # Otherwise, begin a depth first search of all nodes reachable from
#             # the current state
#             frontier = Stack()
#             for dst in iter.substate.available_cost_paths(input):
#                 if dst.id not in explored:
#                     explored.add(dst.id)
#                     frontier.push(dst)
#                     next_state.add_iterator(NFAIterator(dst, iter.age))

#                 # If a the edge leads to the final state, declare a match
#                 if dst.id == self.nfa.end.id:
#                     for age in range(iter.age + 1, self.current_age):
#                         self.age_restrictions.add(age)
#                     match = (iter.age, self.current_age)

#             # Determine the epsilon closure of all destinations advanced from
#             # the previous state
#             while not frontier.is_empty():
#                 sub_state = frontier.top()
#                 frontier.pop()
#                 free_nodes = sub_state.epsilon_paths()
#                 for dst in free_nodes:
#                     if dst.id not in explored:
#                         explored.add(dst.id)
#                         frontier.push(dst)
#                         next_state.add_iterator(NFAIterator(dst, iter.age))
#                         # If the edge leads to the final state, declare a match
#                     if dst.id == self.nfa.end.id:
#                         for age in range(iter.age + 1, self.current_age):
#                             self.age_restrictions.add(age)
#                         match = (iter.age, self.current_age)

#         self.dfa = next_state
#         return match


