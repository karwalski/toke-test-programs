import sys

def replace_quotes(text):
    result = []
    in_double = False
    in_single = False
    for char in text:
        if char == '"':
            if not in_double:
                result.append('\u201c')
                in_double = True
            else:
                result.append('\u201d')
                in_double = False
        elif char == "'":
            if not in_single:
                result.append('\u2018')
                in_single = True
            else:
                result.append('\u2019')
                in_single = False
        else:
            result.append(char)
    return ''.join(result)

text = sys.stdin.read()
if text.endswith('\n'):
    text = text[:-1]
print(replace_quotes(text))