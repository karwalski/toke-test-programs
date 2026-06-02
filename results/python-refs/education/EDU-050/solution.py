import sys
import re

# Read input
lines = sys.stdin.read().strip().split('\n')
vocab_terms = [term.strip() for term in lines[0].split(',')]
text = ' '.join(lines[1:])

# Convert text to lowercase for case-insensitive matching
text_lower = text.lower()

# Count occurrences of each term
term_counts = {}
for term in vocab_terms:
    # Use word boundaries to match whole words only
    pattern = r'\b' + re.escape(term.lower()) + r'\b'
    matches = re.findall(pattern, text_lower)
    count = len(matches)
    if count > 0:
        term_counts[term] = count

# Sort by frequency (descending) then by term name for stable sort
sorted_terms = sorted(term_counts.items(), key=lambda x: (-x[1], x[0]))

# Output results
for term, count in sorted_terms:
    print(f"{term}: {count}")