import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock search history data
    search_history = [
        {"query": "rust programming", "searched_at": "2026-01-01T00:00:00Z"},
        {"query": "@alice", "searched_at": "2025-12-31T00:00:00Z"}
    ]
    
    # Create response
    response = {"searches": search_history}
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()