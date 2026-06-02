import sys

def encode_string(s):
    if not s:
        return ""
    
    result = []
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            result.append(str(count) + current_char)
            current_char = s[i]
            count = 1
    
    result.append(str(count) + current_char)
    return ''.join(result)

def decode_string(s):
    if not s:
        return ""
    
    result = []
    i = 0
    
    while i < len(s):
        # Read the count
        count_str = ""
        while i < len(s) and s[i].isdigit():
            count_str += s[i]
            i += 1
        
        # Read the character
        if i < len(s):
            char = s[i]
            count = int(count_str)
            result.append(char * count)
            i += 1
    
    return ''.join(result)

# Read input
mode = input().strip()
string = input().strip()

# Process based on mode
if mode == "encode":
    print(encode_string(string))
else:  # decode
    print(decode_string(string))