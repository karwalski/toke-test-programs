import json
import sys

def main():
    input_data = json.loads(sys.stdin.read().strip())
    
    action = input_data.get("action")
    region = input_data.get("region")
    limit = input_data.get("limit", 10)
    
    all_trending_queries = [
        {"rank": 1, "query": "world cup", "search_volume": 50000},
        {"rank": 2, "query": "new album", "search_volume": 35000},
    ]
    
    trending_queries = all_trending_queries[:limit]
    
    response = {
        "trending": trending_queries,
        "updated_at": "2026-01-01T00:00:00Z"
    }
    
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()