# Mini Regex

A simple regular expression engine that parses regular expressions, converts them into an
NFA(non-deterministic finite automata) and runs it on input strings to find
matches.   

### Patterns supported: 
  - `ab` -- union
  - `a|b` -- or
  - `a*` -- Kleene star (0 or more matches)
  - `.` -- Metachar
  - `(ab(c|d))|e` -- nested expressions
  - `[^A-Zabc0-9]` -- regex classes with range and negation
  - `?` -- 0 or 1 match
  - `+` -- 1 or more matches
  - `\\.` -- Backslash to escape special chars

### Context Free Grammar for mini regex: 
```
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
```

#### To run tests:
```
$ python3 -m unittest discover -s test/
```  

#### To run example:
```
$ python3 example.py
```

### Implementation Details:
  - Uses a handmade recursive descent parser (because it would be cheating to use
    regular expressions in a parser for regular expressions)
  - As the parser goes through the pattern, it uses thompsons constructions
    (see the wikipedia article linked in thompson_construction.py), to build up
    a Non-Deterministic-Finite-Automata (NFA). [See more here](https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton)
  - A traditional regex only supports the (implicit) concat operator, pipe/union operator, and the
    kleene star operator. To get around this, I use predicate-based
    "transitions" between nodes (see transitions.py) that allows me to support
    things like metachars, and regex character classes. Other ops (+, ?) are
    derived using the three basic operations above.
  - When run, an NFA can be in multiple states simultaneously. Some
    implementations use backtracking to handle this. Instead, I used what I
    called a "DFA State" which holds a set of NFA substates that are
    "active". Each new input character (from the string being searched)
    either kills or advances each substate in this set. When advanced, a
    substate also spawns multiple new substates, for each of the nfa's nodes
    reachable by only epsilon transitions from the current node.
    "epsilon" transitions. 
  - If at anypoint the DFAState holds a substate that is the NFA's endstate,
    the DFARunner has found a "matching string".
  - If at anypoint the DFAState no longer holds any active substates, the
    DFARunner is completed
  - The is_greedy property of the MiniRegex class (true by default) determines
    whether the DFARunner needs to be "complete" before returning a match that
    has been found. 

#### TODO:
  - groups
  - ^ match at the beginning
  - $ match at the end of the string$
  - \w, \W, \b...etc whitespace and newline escapes

