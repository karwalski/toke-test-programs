import sys

for line in sys.stdin:
    phrase = line.strip()
    if phrase:
        words = phrase.split()
        acronym = ''.join(word[0].upper() for word in words)
        print(acronym)