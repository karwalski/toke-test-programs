import sys
from collections import Counter
import re

def clean_text(text):
    # Convert to lowercase and split into words, removing punctuation
    words = re.findall(r'\b\w+\b', text.lower())
    return words

def calculate_similarity(text1, text2):
    words1 = clean_text(text1)
    words2 = clean_text(text2)
    
    if not words1 and not words2:
        return 100.0
    if not words1 or not words2:
        return 0.0
    
    counter1 = Counter(words1)
    counter2 = Counter(words2)
    
    # Calculate Jaccard similarity
    intersection = sum((counter1 & counter2).values())
    union = sum((counter1 | counter2).values())
    
    if union == 0:
        return 100.0
    
    similarity = (intersection / union) * 100
    return similarity

# Read all input
input_text = sys.stdin.read().strip()

# Split by '===' separator
blocks = input_text.split('===')

# First block is the submission
submission = blocks[0].strip()

# Remaining blocks are references
references = [block.strip() for block in blocks[1:] if block.strip()]

flagged = False

for i, reference in enumerate(references):
    similarity = calculate_similarity(submission, reference)
    print(f"Reference {i+1}: {similarity:.0f}% similar")
    
    if similarity > 30:
        flagged = True

if flagged:
    print("FLAGGED: Similarity exceeds 30%")