import sys

def replace_quotes(text):
    result = []
    in_double_quote = False
    in_single_quote = False
    
    for char in text:
        if char == '"':
            if not in_double_quote:
                result.append('"')
                in_double_quote = True
            else:
                result.append('"')
                in_double_quote = False
        elif char == "'":
            if not in_single_quote:
                result.append(''')
                in_single_quote = True
            else:
                result.append(''')
                in_single_quote = False
        else:
            result.append(char)
    
    return ''.join(result)

# Read from stdin
text = sys.stdin.read().strip()

# Replace quotes and print
print(replace_quotes(text))