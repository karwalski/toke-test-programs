import sys
import re

# Read threshold
threshold = int(input().strip())

# Read all remaining text
text = ""
try:
    while True:
        line = input()
        text += line + " "
except EOFError:
    pass

# Split into sentences using regex
sentences = re.split(r'[.!?]+', text.strip())

# Process each sentence
sentence_num = 0
for sentence in sentences:
    sentence = sentence.strip()
    if sentence:  # Skip empty sentences
        sentence_num += 1
        words = sentence.split()
        word_count = len(words)
        
        if word_count > threshold:
            print(f"Sentence {sentence_num} ({word_count} words): {sentence}.")