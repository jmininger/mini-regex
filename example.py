from src import regex

pattern = '.el*o'
regex = regex.MiniRegex(pattern)
search_str = 'Hello World!'
result = regex.first_match(search_str)
print(result)  # (0, 4)
