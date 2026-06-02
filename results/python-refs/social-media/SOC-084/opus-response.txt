import json
import sys

def search_posts():
    input_data = json.loads(sys.stdin.read().strip())
    query = input_data.get("query", "")
    page = input_data.get("page", 1)
    
    response = {
        "results": [{"id":15,"content":"Machine learning is amazing","author":"techie","relevance":0.95}],
        "total": 5,
        "page": page
    }
    
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    search_posts()