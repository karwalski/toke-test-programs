import json
import sys

# Predefined data for autocomplete suggestions
SUGGESTIONS_DATA = {
    "mac": [
        {"type": "query", "text": "machine learning"},
        {"type": "user", "text": "@macdev"},
        {"type": "hashtag", "text": "#macos"}
    ],
    "python": [
        {"type": "query", "text": "python programming"},
        {"type": "user", "text": "@pythonista"},
        {"type": "hashtag", "text": "#python"}
    ],
    "data": [
        {"type": "query", "text": "data science"},
        {"type": "user", "text": "@dataexpert"},
        {"type": "hashtag", "text": "#database"}
    ]
}

def get_suggestions(partial_query):
    partial_query = partial_query.lower().strip()
    
    # Find matching suggestions
    suggestions = []
    for key, values in SUGGESTIONS_DATA.items():
        if key.startswith(partial_query):
            suggestions.extend(values)
    
    return suggestions

# Read input from stdin
input_line = sys.stdin.read().strip()
request = json.loads(input_line)

# Process the request
if request.get("action") == "search_suggest":
    partial_query = request.get("partial_query", "")
    suggestions = get_suggestions(partial_query)
    
    response = {"suggestions": suggestions}
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))