import json
import sys
import re

def calculate_similarity(text1, text2):
    def tokenize(text):
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
    filtered_chunks = [chunk for chunk in chunks if chunk['score'] >= min_score]
    filtered_chunks.sort(key=lambda x: x['score'], reverse=True)
    
    final_chunks = []
    for chunk in filtered_chunks:
        is_redundant = False
        for existing_chunk in final_chunks:
            similarity = calculate_similarity(chunk['text'], existing_chunk['text'])
            if similarity >= max_redundancy:
                is_redundant = True
                break
        if not is_redundant:
            final_chunks.append(chunk)
    
    return [chunk['id'] for chunk in final_chunks]

input_data = json.loads(sys.stdin.read().strip())
chunks = input_data['chunks']
min_score = input_data['min_score']
max_redundancy = input_data['max_redundancy']
result = filter_chunks(chunks, min_score, max_redundancy)
print(json.dumps(result, separators=(',', ':')))