shift = int(input())
text = input()

result = ""
for char in text:
    if char.isalpha():
        # Determine if uppercase or lowercase
        if char.isupper():
            # Shift within A-Z range
            shifted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            # Shift within a-z range
            shifted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        result += shifted
    else:
        # Non-alphabetic characters remain unchanged
        result += char

print(result)