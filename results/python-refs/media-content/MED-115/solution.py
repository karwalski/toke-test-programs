import sys

encoded = input().strip()
result = ""
i = 0

while i < len(encoded):
    # Read the number
    num_str = ""
    while i < len(encoded) and encoded[i].isdigit():
        num_str += encoded[i]
        i += 1
    
    # Read the character
    if i < len(encoded):
        char = encoded[i]
        count = int(num_str)
        result += char * count
        i += 1

print(result)