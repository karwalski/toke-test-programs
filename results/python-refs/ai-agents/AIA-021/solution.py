import json
import sys

def reciprocal_rank_fusion(keyword_results, semantic_results, k=60):
    """
    Apply reciprocal rank fusion to merge two ranked lists.
    RRF score = sum(1 / (k + rank)) for each list where doc appears
    """
    scores = {}
    
    # Calculate scores from keyword results
    for rank, doc_id in enumerate(keyword_results, 1):
        if doc_id not in scores:
            scores[doc_id] = 0
        scores[doc_id] += 1 / (k + rank)
    
    # Calculate scores from semantic results
    for rank, doc_id in enumerate(semantic_results, 1):
        if doc_id not in scores:
            scores[doc_id] = 0
        scores[doc_id] += 1 / (k + rank)
    
    # Sort by score (descending) and return doc ids
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [doc_id for doc_id, score in sorted_docs]

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

keyword_results = input_data["keyword_results"]
semantic_results = input_data["semantic_results"]
k = input_data.get("k", 60)

# Apply reciprocal rank fusion
fused_results = reciprocal_rank_fusion(keyword_results, semantic_results, k)

# Output as JSON array
print(json.dumps(fused_results, separators=(',', ':')))