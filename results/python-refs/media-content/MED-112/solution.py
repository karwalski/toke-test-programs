import sys
import re

def tokenize(text):
    tokens = []
    i = 0
    while i < len(text):
        char = text[i]
        
        if char.isalpha():
            # Word token
            word = ''
            while i < len(text) and text[i].isalpha():
                word += text[i]
                i += 1
            tokens.append(('WORD', word))
        elif char.isdigit():
            # Number token
            num = ''
            while i < len(text) and text[i].isdigit():
                num += text[i]
                i += 1
            tokens.append(('NUM', num))
        elif char.isspace():
            # Whitespace token
            space = ''
            while i < len(text) and text[i].isspace():
                space += text[i]
                i += 1
            tokens.append(('SPACE', space))
        else:
            # Punctuation token
            tokens.append(('PUNCT', char))
            i += 1
    
    return tokens

# Read input from stdin
text = sys.stdin.read().strip()

# Tokenize and output
tokens = tokenize(text)
for token_type, value in tokens:
    print(f"{token_type}: {value}")