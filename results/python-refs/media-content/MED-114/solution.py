import sys

text = sys.stdin.read().strip()

if not text:
    print("")
else:
    result = []
    current_char = text[0]
    count = 1
    
    for i in range(1, len(text)):
        if text[i] == current_char:
            count += 1
        else:
            result.append(str(count) + current_char)
            current_char = text[i]
            count = 1
    
    result.append(str(count) + current_char)
    print(''.join(result))