import json
import sys
from collections import Counter
import re

def calculate_similarity(text1, text2):
    # Simple token-based Jaccard similarity
    def tokenize(text):
        # Convert to lowercase and extract words
        words = re.findall(r'\b\w+\b', text.lower())
        return set(words)
    
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    
    if not tokens1 and not tokens2:
        return 1.0
    if not tokens1 or not tokens2:
        return 0.0
    
    intersection = len(tokens1.intersection(tokens2))
    union = len(tokens1.union(tokens2))
    
    return intersection / union

def filter_chunks(chunks, min_score, max_redundancy):
    # Filter by minimum score
    filtered_chunks = [chunk for chunk in chunks if chunk['score'] >= min_score]
    
    # Sort by score descending to prioritize higher-scored chunks
    filtered_chunks.sort(key=lambda x: x['score'], reverse=True)
    
    # Remove redundant chunks
    final_chunks = []
    
    for chunk in filtered_chunks:
        is_redundant = False
        
        for existing_chunk in final_chunks:
            similarity = calculate_similarity(chunk['text'], existing_chunk['text'])
            if similarity > max_redundancy:
                is_redundant = True
                break
        
        if not is_redundant:
            final_chunks.append(chunk)
    
    # Return chunk IDs in original order
    final_ids = [chunk['id'] for chunk in final_chunks]
    return final_ids

# Read input
input_data = json.loads(sys.stdin.read().strip())

chunks = input_data['chunks']
min_score = input_data['min_score']
max_redundancy = input_data['max_redundancy']

# Filter chunks
result = filter_chunks(chunks, min_score, max_redundancy)

# Output result
print(json.dumps(result, separators=(',', ':')))