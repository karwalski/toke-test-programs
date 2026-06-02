import sys
import re

text = sys.stdin.read().strip()

# Split on sentence endings followed by whitespace
sentences = re.split(r'([.!?]+\s*)', text)

result = []
for i, part in enumerate(sentences):
    if i % 2 == 0 and part:  # This is actual sentence content (not punctuation)
        # Capitalize first letter of the sentence
        part = part.lstrip()
        if part:
            part = part[0].upper() + part[1:].lower()
        result.append(part)
    else:  # This is punctuation and whitespace
        result.append(part)

print(''.join(result))