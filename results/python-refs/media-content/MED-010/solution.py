import sys

lines = sys.stdin.read().strip().split('\n')
dictionary_words = set(lines[0].split(','))
text_lines = lines[1:]

seen_misspelled = set()
misspelled_order = []

for line in text_lines:
    words = line.split()
    for word in words:
        if word not in dictionary_words and word not in seen_misspelled:
            seen_misspelled.add(word)
            misspelled_order.append(word)

for word in misspelled_order:
    print(word)