# Mini Regex

A simple regular expression engine that parses regular expressions, converts them into an
NFA(non-deterministic finite automata) and runs it on input strings to find
matches.   

###Patterns supported: 
  - `ab` -- union
  - `a|b` -- or
  - `a*` -- Kleene star (0 or more matches)
  - `.` -- Metachar
  - `(ab(c|d))|e` -- nested expressions
  - `\[^A-Zabc0-9]` -- regex classes with range and negation
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

####To run tests:
```
$ python3 -m unittest discover -s test/
```  

####To run example:
```
$ python3 example.py
```

#### TODO:
  - groups
  - ^ match at the beginning
  - $ match at the end of the string$
  - \w, \W, \b..etc whitespace and newline escapes


