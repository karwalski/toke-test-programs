import sys
import re

text = sys.stdin.read().strip()

# Split on sentence boundaries (periods, exclamation marks, question marks)
# followed by whitespace or end of string
sentences = re.split(r'([.!?])\s*', text)

result = []
i = 0
while i < len(sentences):
    if sentences[i].strip():  # Non-empty sentence content
        sentence = sentences[i]
        if i + 1 < len(sentences) and sentences[i + 1] in '.!?':
            # Add the punctuation back
            sentence += sentences[i + 1]
            i += 2
        else:
            i += 1
        result.append(f"<S>{sentence}</S>")
    else:
        i += 1

print(" ".join(result))