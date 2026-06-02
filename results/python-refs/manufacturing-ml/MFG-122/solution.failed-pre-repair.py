import sys
import json
import math

def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(a * a for a in vec2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

# Read all input
input_data = sys.stdin.read().strip()

# Split by ---
parts = input_data.split('---')
historical_part = parts[0].strip()
test_part = parts[1].strip()

# Parse historical batches
historical_lines = historical_part.split('\n')
header = historical_lines[0]
historical_batches = []

for line in historical_lines[1:]:
    values = line.split(',')
    batch_name = values[0]
    features = [float(x) for x in values[1:]]
    historical_batches.append((batch_name, features))

# Parse test batch
test_features = [float(x) for x in test_part.split(',')]

# Calculate similarities
similarities = []
best_similarity = -1
best_match = ""

for batch_name, features in historical_batches:
    similarity = cosine_similarity(features, test_features)
    similarities.append({
        "batch": batch_name,
        "similarity": round(similarity, 2)
    })
    
    if similarity > best_similarity:
        best_similarity = similarity
        best_match = batch_name

# Create output
result = {
    "similarities": similarities,
    "best_match": best_match
}

print(json.dumps(result, separators=(',', ':')))