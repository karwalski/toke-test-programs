import sys

rle_string = input().strip()
result = ""
i = 0

while i < len(rle_string):
    # Read the number
    num_str = ""
    while i < len(rle_string) and rle_string[i].isdigit():
        num_str += rle_string[i]
        i += 1
    
    # Read the character
    if i < len(rle_string):
        char = rle_string[i]
        count = int(num_str)
        result += char * count
        i += 1

print(result)