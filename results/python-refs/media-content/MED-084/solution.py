import sys

line_num = 1
for line in sys.stdin:
    words = line.strip().split()
    prev_word = None
    
    for word in words:
        if word == prev_word:
            print(f'Line {line_num}: repeated word "{word}"')
        prev_word = word
    
    line_num += 1