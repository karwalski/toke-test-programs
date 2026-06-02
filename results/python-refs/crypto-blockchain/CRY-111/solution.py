import sys
import math
from collections import Counter

# Read input
text = input().strip()

# Count character frequencies
char_counts = Counter(text)
total_chars = len(text)

# Calculate Shannon entropy
entropy = 0.0
if total_chars > 0:
    for count in char_counts.values():
        probability = count / total_chars
        if probability > 0:
            entropy -= probability * math.log2(probability)

# Output with 2 decimal places
print(f"{entropy:.2f}")