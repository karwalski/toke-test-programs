mode = input().strip()
shift = int(input().strip())
text = input()

def caesar_cipher(text, shift, encrypt=True):
    if not encrypt:
        shift = -shift
    
    result = ""
    for char in text:
        if char.isalpha():
            # Determine if uppercase or lowercase
            is_upper = char.isupper()
            char = char.lower()
            
            # Apply shift
            shifted = ord(char) - ord('a')
            shifted = (shifted + shift) % 26
            new_char = chr(shifted + ord('a'))
            
            # Restore case
            if is_upper:
                new_char = new_char.upper()
            
            result += new_char
        else:
            result += char
    
    return result

if mode == "encrypt":
    output = caesar_cipher(text, shift, True)
else:  # decrypt
    output = caesar_cipher(text, shift, False)

print(output)