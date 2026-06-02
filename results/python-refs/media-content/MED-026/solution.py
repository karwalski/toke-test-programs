import sys
import re

text = sys.stdin.read().strip()
sentences = re.split(r'(?<=[.!?])\s+', text)

for sentence in sentences:
    if sentence.strip():
        print(sentence.strip())