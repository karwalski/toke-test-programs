import sys
from collections import defaultdict

# Read all input
lines = []
for line in sys.stdin:
    line = line.strip()
    if line:
        lines.append(line)

# Build inverted index
index = defaultdict(set)

for line in lines:
    # Parse "DOC id: text" format
    parts = line.split(': ', 1)
    if len(parts) == 2:
        doc_part = parts[0]
        text = parts[1]
        
        # Extract doc ID
        doc_id = int(doc_part.split()[1])
        
        # Process words in text
        words = text.split()
        for word in words:
            index[word].add(doc_id)

# Sort words alphabetically and output
for word in sorted(index.keys()):
    doc_ids = sorted(list(index[word]))
    print(f"{word} -> {doc_ids}")