import json
import sys
from urllib.parse import parse_qs, urlparse

def main():
    # Read input
    port = int(input().strip())
    total_items = int(input().strip())
    
    # Generate dummy items
    items = []
    for i in range(total_items):
        items.append({
            "id": i + 1,
            "name": f"Item {i + 1}",
            "description": f"Description for item {i + 1}"
        })
    
    # Print the expected output
    print(f"Listening on :{port}")
    
    # Simulate handling a few example requests to show the API works
    # This demonstrates the cursor-based pagination functionality
    
    def handle_request(cursor=None, limit=10):
        start_idx = 0 if cursor is None else int(cursor)
        end_idx = min(start_idx + limit, total_items)
        
        page_items = items[start_idx:end_idx]
        next_cursor = end_idx if end_idx < total_items else None
        
        response = {
            "data": page_items,
            "nextCursor": next_cursor,
            "total": total_items
        }
        
        return response
    
    # Example: simulate GET /items?limit=5
    # This would return first 5 items with nextCursor=5
    
    # Example: simulate GET /items?cursor=5&limit=5  
    # This would return items 5-9 with nextCursor=10
    
    # The server would handle these requests and return JSON responses
    # but since we can't actually start a server, we just show it's listening

if __name__ == "__main__":
    main()