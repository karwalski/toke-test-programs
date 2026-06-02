import sys

# Read all input
content = sys.stdin.read().strip()

# Split by the separator
parts = content.split('---')
doc1 = parts[0].strip()
doc2 = parts[1].strip()

# Split into words and create sets
words1 = set(doc1.split())
words2 = set(doc2.split())

# Calculate Jaccard similarity
intersection = len(words1 & words2)
union = len(words1 | words2)

if union == 0:
    similarity = 0.0
else:
    similarity = intersection / union

# Output with exactly 3 decimal places
print(f"similarity: {similarity:.3f}")