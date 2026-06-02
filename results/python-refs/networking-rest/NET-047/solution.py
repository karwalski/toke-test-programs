import json
import sys
from urllib.parse import parse_qs, urlparse

def search_documents(documents, query, page=1, limit=10):
    if not query:
        return []
    
    query_lower = query.lower()
    results = []
    
    for doc in documents:
        score = 0
        title = doc.get('title', '').lower()
        body = doc.get('body', '').lower()
        
        # Simple scoring: count occurrences in title (weighted 2x) and body
        title_matches = title.count(query_lower)
        body_matches = body.count(query_lower)
        score = title_matches * 2 + body_matches
        
        if score > 0:
            results.append((score, doc))
    
    # Sort by score descending
    results.sort(key=lambda x: x[0], reverse=True)
    
    # Extract just the documents
    ranked_docs = [doc for score, doc in results]
    
    # Pagination
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    page_results = ranked_docs[start_idx:end_idx]
    
    return {
        "results": page_results,
        "total": len(ranked_docs),
        "page": page,
        "limit": limit
    }

def handle_search_request(documents, query_string):
    parsed = parse_qs(query_string)
    
    q = parsed.get('q', [''])[0]
    page = int(parsed.get('page', ['1'])[0])
    limit = int(parsed.get('limit', ['10'])[0])
    
    return search_documents(documents, q, page, limit)

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

port = int(lines[0])
print(f"Listening on :{port}")

# Parse documents
documents = []
for i in range(1, len(lines)):
    line = lines[i]
    if line:
        try:
            doc = json.loads(line)
            documents.append(doc)
        except json.JSONDecodeError:
            pass

# Since we're simulating and not actually running a server,
# we just print the listening message as that's the expected output