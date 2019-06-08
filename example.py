from mini_regex.regex import MiniRegex
# from mini_regex.util import nfa_to_table


# Supported Special Chars:

# Repeaters: ?, +, *
# Metachar: .
# Union: |
# RegexClasses (with ranges and negation):  [^0-10abc]
# Escaping special chars with double slash: \\

# Also supported:
# - Greedy toggle on regex class (currently only works for find_all_matches())


# Example1: Simple Pattern
pattern = '.el*o'
regex = MiniRegex(pattern)
search_str = 'Hello World!'
result = regex.find_all_matches(search_str)
print(result)  # [MatchObj: Hello (0, 4)]


# Example 2: Find All Gmail accounts in a string
regex2 = MiniRegex("[a-zA-Z0-9.]+@gmail\\.com")
search_str = '''
Name: John Doe
Age: 21
email: johndoe@gmail.com
interests: coding

Name: JaneDoe
Age: 18
email: jane.doe@notgmail.com
interests: none

Name: Guido Van Rossum
Age: 63
email: guido.van.rossum@gmail.com
interests: Python!!!
'''

result = regex2.find_all_matches(search_str)
print(result)
# [MatchObj: johndoe@gmail.com (31, 47),
#  MatchObj: guido.van.rossum@gmail.com (174, 199)]


# Example 3: Finding the first gmail in a string, and interacting with a match
# object
match = regex2.first_match(search_str)
if match.has_value():
    print("Result span:", match.get_span())
    print("Result value: ", match.get_value())
# (31, 47)
# johndoe@gmail.com
