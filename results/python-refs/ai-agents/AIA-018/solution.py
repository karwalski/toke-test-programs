import json
import sys

def solve_chunk_selection(data):
    chunks = data['chunks']
    max_tokens = data['max_tokens']
    
    # Sort chunks by relevance score in descending order
    sorted_chunks = sorted(chunks, key=lambda x: x['relevance_score'], reverse=True)
    
    selected = []
    total_tokens = 0
    
    # Greedy selection: pick highest relevance chunks that fit
    for chunk in sorted_chunks:
        if total_tokens + chunk['token_count'] <= max_tokens:
            selected.append(chunk['id'])
            total_tokens += chunk['token_count']
    
    utilisation = total_tokens / max_tokens if max_tokens > 0 else 0.0
    
    return {
        "selected": selected,
        "total_tokens": total_tokens,
        "utilisation": utilisation
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Solve and output result
result = solve_chunk_selection(input_data)
print(json.dumps(result, separators=(',', ':')))