import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read())

# Dictionary to store the best passage for each source document
best_passages = {}

# Process each passage
for passage in input_data:
    source_doc = passage["source_doc"]
    relevance_score = passage["relevance_score"]
    
    # If this is the first passage from this source or has better relevance score
    if source_doc not in best_passages or relevance_score > best_passages[source_doc]["relevance_score"]:
        best_passages[source_doc] = passage

# Convert to list and output as JSON
result = list(best_passages.values())
print(json.dumps(result, separators=(',', ':')))