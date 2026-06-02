import sys
import re

# Read input
lines = sys.stdin.read().strip().split('\n')
keywords = [k.strip() for k in lines[0].split(',')]
text = ' '.join(lines[1:])

# Convert to lowercase for case-insensitive matching
text_lower = text.lower()
keywords_lower = [k.lower() for k in keywords]

# Split text into words
words = re.findall(r'\b\w+\b', text_lower)
total_words = len(words)

# Calculate keyword densities
densities = []
for keyword in keywords_lower:
    count = words.count(keyword)
    density = (count / total_words) * 100 if total_words > 0 else 0
    densities.append((keyword, density))

# Sort by density descending
densities.sort(key=lambda x: x[1], reverse=True)

# Output results
for keyword, density in densities:
    print(f"{keyword}: {density}%")