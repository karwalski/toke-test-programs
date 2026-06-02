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

input_data = sys.stdin.read().strip()
parts = input_data.split('---')
historical_part = parts[0].strip()
test_part = parts[1].strip()

historical_lines = historical_part.split('\n')
historical_batches = []

for line in historical_lines[1:]:
    line = line.strip()
    if not line:
        continue
    values = line.split(',')
    batch_name = values[0]
    features = [float(x) for x in values[1:]]
    historical_batches.append((batch_name, features))

# test_part may contain header-less line, possibly with batch name or not
test_lines = [l.strip() for l in test_part.split('\n') if l.strip()]
test_line = test_lines[-1]
test_values = test_line.split(',')
# Try parsing all as floats; if first fails, skip it
try:
    test_features = [float(x) for x in test_values]
except ValueError:
    test_features = [float(x) for x in test_values[1:]]

similarities = []
best_similarity = -1
best_match = ""

for batch_name, features in historical_batches:
    similarity = cosine_similarity(features, test_features)
    rounded = round(similarity, 2)
    similarities.append({
        "batch": batch_name,
        "similarity": rounded
    })
    if similarity > best_similarity:
        best_similarity = similarity
        best_match = batch_name

result = {
    "similarities": similarities,
    "best_match": best_match
}

print(json.dumps(result, separators=(',', ':')))