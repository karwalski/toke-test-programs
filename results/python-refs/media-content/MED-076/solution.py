import sys

def rot13(text):
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            # Rotate lowercase letters
            result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= char <= 'Z':
            # Rotate uppercase letters
            result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
        else:
            # Keep non-alphabetic characters unchanged
            result.append(char)
    return ''.join(result)

# Read input from stdin
text = input()

# Apply ROT13 and print result
print(rot13(text))