import json
import sys
import re
from collections import defaultdict
import math

def calculate_relevance(query_terms, content):
    """Calculate relevance score using TF-IDF-like approach"""
    content_lower = content.lower()
    query_lower = [term.lower() for term in query_terms]
    
    # Count term frequencies in content
    content_words = re.findall(r'\b\w+\b', content_lower)
    content_word_count = len(content_words)
    
    if content_word_count == 0:
        return 0.0
    
    # Calculate term frequency score
    tf_score = 0.0
    for term in query_lower:
        term_count = content_lower.count(term)
        if term_count > 0:
            # Term frequency with normalization
            tf = term_count / content_word_count
            # Add bonus for exact matches
            if term in content_words:
                tf_score += tf * 2
            else:
                tf_score += tf
    
    # Normalize by query length
    if len(query_lower) > 0:
        tf_score = tf_score / len(query_lower)
    
    # Cap at 1.0 and round to 2 decimal places
    return min(1.0, round(tf_score, 2))

def search_posts():
    # Sample posts database
    posts = [
        {"id": 1, "content": "Python programming is fun", "author": "coder123"},
        {"id": 2, "content": "Data science with machine learning", "author": "datascientist"},
        {"id": 3, "content": "Web development using Django", "author": "webdev"},
        {"id": 4, "content": "Deep learning neural networks", "author": "airesearcher"},
        {"id": 5, "content": "Machine learning algorithms and models", "author": "mlexpert"},
        {"id": 15, "content": "Machine learning is amazing", "author": "techie"},
        {"id": 6, "content": "JavaScript frontend development", "author": "frontend"},
        {"id": 7, "content": "Database design and optimization", "author": "dbadmin"},
        {"id": 8, "content": "Mobile app development", "author": "mobiledev"},
        {"id": 9, "content": "Cloud computing and AWS", "author": "cloudarch"},
        {"id": 10, "content": "Artificial intelligence and machine learning trends", "author": "futurist"}
    ]
    
    # Read input
    input_data = json.loads(sys.stdin.read().strip())
    
    query = input_data.get("query", "")
    page = input_data.get("page", 1)
    limit = input_data.get("limit", 20)
    
    # Parse query terms
    query_terms = re.findall(r'\b\w+\b', query)
    
    # Find matching posts and calculate relevance
    matches = []
    for post in posts:
        relevance = calculate_relevance(query_terms, post["content"])
        if relevance > 0:
            matches.append({
                "id": post["id"],
                "content": post["content"],
                "author": post["author"],
                "relevance": relevance
            })
    
    # Sort by relevance (descending)
    matches.sort(key=lambda x: x["relevance"], reverse=True)
    
    # Apply pagination
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_results = matches[start_idx:end_idx]
    
    # Prepare response
    response = {
        "results": paginated_results,
        "total": len(matches),
        "page": page
    }
    
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    search_posts()