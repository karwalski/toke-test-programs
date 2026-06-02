mode = input().strip()
key = input().strip()
text = input().strip()

def vigenere_encrypt(text, key):
    result = ""
    key_index = 0
    
    for char in text:
        if char.isalpha():
            # Convert to uppercase
            char = char.upper()
            key_char = key[key_index % len(key)].upper()
            
            # Encrypt using Vigenère formula
            encrypted_char = chr((ord(char) - ord('A') + ord(key_char) - ord('A')) % 26 + ord('A'))
            result += encrypted_char
            key_index += 1
        else:
            result += char
    
    return result

def vigenere_decrypt(text, key):
    result = ""
    key_index = 0
    
    for char in text:
        if char.isalpha():
            # Convert to uppercase
            char = char.upper()
            key_char = key[key_index % len(key)].upper()
            
            # Decrypt using Vigenère formula
            decrypted_char = chr((ord(char) - ord('A') - (ord(key_char) - ord('A'))) % 26 + ord('A'))
            result += decrypted_char
            key_index += 1
        else:
            result += char
    
    return result

if mode == "encrypt":
    print(vigenere_encrypt(text, key))
else:
    print(vigenere_decrypt(text, key))