import json
import sys
import math

def cosine_similarity(vec1, vec2):
    # Calculate dot product
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # Calculate magnitudes
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(a * a for a in vec2))
    
    # Handle zero magnitude case
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

def solve(data):
    query_vector = data['query_vector']
    documents = data['documents']
    top_k = data['top_k']
    
    # Calculate similarities for all documents
    similarities = []
    for doc in documents:
        doc_id = doc['id']
        doc_vector = doc['vector']
        similarity = cosine_similarity(query_vector, doc_vector)
        similarities.append({'id': doc_id, 'similarity': similarity})
    
    # Sort by similarity descending
    similarities.sort(key=lambda x: x['similarity'], reverse=True)
    
    # Return top k results
    return similarities[:top_k]

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())
result = solve(input_data)
print(json.dumps(result, separators=(',', ':')))