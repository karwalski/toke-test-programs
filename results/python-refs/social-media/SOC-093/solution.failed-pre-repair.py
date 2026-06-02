import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Parse the request
    action = input_data.get("action")
    region = input_data.get("region")
    limit = input_data.get("limit", 10)
    
    # Simulate trending search queries data
    # In a real implementation, this would come from a database or API
    all_trending_queries = [
        {"rank": 1, "query": "world cup", "search_volume": 50000},
        {"rank": 2, "query": "new album", "search_volume": 35000},
        {"rank": 3, "query": "weather forecast", "search_volume": 28000},
        {"rank": 4, "query": "movie reviews", "search_volume": 25000},
        {"rank": 5, "query": "tech news", "search_volume": 22000},
        {"rank": 6, "query": "stock market", "search_volume": 20000},
        {"rank": 7, "query": "recipe ideas", "search_volume": 18000},
        {"rank": 8, "query": "travel deals", "search_volume": 15000},
        {"rank": 9, "query": "fitness tips", "search_volume": 12000},
        {"rank": 10, "query": "crypto prices", "search_volume": 10000}
    ]
    
    # Get the trending queries based on the limit
    trending_queries = all_trending_queries[:limit]
    
    # Create the response
    response = {
        "trending": trending_queries,
        "updated_at": "2026-01-01T00:00:00Z"
    }
    
    # Output the JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()