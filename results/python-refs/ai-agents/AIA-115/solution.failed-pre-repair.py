import json
import sys

def calculate_combined_score(item):
    # Using weighted average: recency=0.3, relevance=0.4, importance=0.3
    recency = item['recency_score']
    relevance = item['relevance_score']
    importance = item['importance_score']
    
    combined = 0.3 * recency + 0.4 * relevance + 0.3 * importance
    return round(combined, 2)

def solve_memory_prioritization(input_data):
    items = input_data['items']
    max_items = input_data['max_items']
    
    # Calculate combined scores for all items
    scoring = []
    for item in items:
        combined_score = calculate_combined_score(item)
        scoring.append({
            'id': item['id'],
            'combined_score': combined_score
        })
    
    # Sort by combined score (descending)
    scoring.sort(key=lambda x: x['combined_score'], reverse=True)
    
    # Determine retained and evicted items
    retained = [item['id'] for item in scoring[:max_items]]
    evicted = [item['id'] for item in scoring[max_items:]]
    
    return {
        'retained': retained,
        'evicted': evicted,
        'scoring': scoring
    }

# Read input from stdin
input_text = sys.stdin.read().strip()
input_data = json.loads(input_text)

# Solve the problem
result = solve_memory_prioritization(input_data)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))