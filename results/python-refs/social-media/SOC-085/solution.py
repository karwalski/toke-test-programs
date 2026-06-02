import json
import sys
from datetime import datetime

def main():
    # Sample data - in a real application this would come from a database
    posts = [
        {"id": 18, "content": "Learning rust programming", "author": "bob", "likes": 5, "has_media": False, "date": "2025-12-15"},
        {"id": 19, "content": "Python vs rust comparison", "author": "charlie", "likes": 8, "has_media": False, "date": "2025-12-20"},
        {"id": 20, "content": "Rust with images", "author": "alice", "likes": 15, "has_media": True, "date": "2026-01-05"},
        {"id": 21, "content": "Rust performance benchmarks", "author": "alice", "likes": 12, "has_media": False, "date": "2026-01-10"},
        {"id": 22, "content": "Beautiful sunset photo", "author": "alice", "likes": 20, "has_media": True, "date": "2026-01-03"}
    ]
    
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())
    
    action = input_data.get("action")
    query = input_data.get("query", "").lower()
    filters = input_data.get("filters", {})
    
    if action == "search_advanced":
        results = []
        
        for post in posts:
            # Check if post matches query
            if query and query not in post["content"].lower():
                continue
            
            # Apply filters
            if "from_user" in filters and post["author"] != filters["from_user"]:
                continue
            
            if "has_media" in filters and post["has_media"] != filters["has_media"]:
                continue
            
            if "min_likes" in filters and post["likes"] < filters["min_likes"]:
                continue
            
            if "date_from" in filters:
                post_date = datetime.strptime(post["date"], "%Y-%m-%d")
                filter_date = datetime.strptime(filters["date_from"], "%Y-%m-%d")
                if post_date < filter_date:
                    continue
            
            # If we get here, the post matches all criteria
            result = {
                "id": post["id"],
                "content": post["content"],
                "author": post["author"],
                "likes": post["likes"],
                "has_media": post["has_media"]
            }
            results.append(result)
        
        response = {
            "results": results,
            "total": len(results)
        }
        
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()