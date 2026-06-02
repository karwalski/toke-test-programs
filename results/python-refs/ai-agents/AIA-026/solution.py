import json
import sys
import re

def calculate_similarity(query, index_info):
    """Calculate similarity between query and index based on keywords and context"""
    query_lower = query.lower()
    description_lower = index_info['description'].lower()
    doc_types = [dt.lower() for dt in index_info['doc_types']]
    
    # Define keyword mappings for different domains
    tech_keywords = ['configure', 'nginx', 'server', 'code', 'programming', 'api', 'tutorial', 'install', 'setup', 'deploy', 'build', 'debug', 'database', 'web', 'software', 'development', 'framework', 'library', 'documentation', 'config', 'technical']
    hr_keywords = ['policy', 'benefits', 'employee', 'hr', 'human resources', 'vacation', 'leave', 'salary', 'payroll', 'insurance', 'handbook', 'personnel', 'hiring', 'onboarding', 'training', 'compliance']
    
    score = 0.0
    
    # Check for direct keyword matches in query
    tech_matches = sum(1 for keyword in tech_keywords if keyword in query_lower)
    hr_matches = sum(1 for keyword in hr_keywords if keyword in query_lower)
    
    # Check if description contains relevant keywords
    if 'programming' in description_lower or 'code' in description_lower or 'technical' in description_lower:
        score += tech_matches * 0.3
    elif 'hr' in description_lower or 'policy' in description_lower or 'benefits' in description_lower:
        score += hr_matches * 0.3
    
    # Check doc types relevance
    if any(doc_type in ['tutorials', 'api_refs', 'documentation'] for doc_type in doc_types):
        score += tech_matches * 0.4
    elif any(doc_type in ['policies', 'handbook'] for doc_type in doc_types):
        score += hr_matches * 0.4
    
    # Specific nginx/configuration bonus
    if 'nginx' in query_lower or 'configure' in query_lower:
        if 'programming' in description_lower or 'tutorials' in doc_types:
            score += 0.5
    
    return min(score, 1.0)

def route_query(data):
    """Route query to most appropriate index"""
    query = data['query']
    indices = data['indices']
    
    best_index = None
    best_score = 0.0
    
    for index in indices:
        score = calculate_similarity(query, index)
        if score > best_score:
            best_score = score
            best_index = index['name']
    
    # Ensure we always select an index, default to first if no good match
    if best_index is None:
        best_index = indices[0]['name']
        best_score = 0.1
    
    # Normalize confidence score
    confidence = min(max(best_score, 0.1), 0.95)
    
    return {
        "selected_index": best_index,
        "confidence": confidence
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Process the query
result = route_query(input_data)

# Output result to stdout
print(json.dumps(result, separators=(',', ':')))