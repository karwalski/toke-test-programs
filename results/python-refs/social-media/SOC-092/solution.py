import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    query = input_data.get("query")
    filters = input_data.get("filters")
    notify = input_data.get("notify")
    
    # Process save_search action
    if action == "save_search":
        # Create response object
        response = {
            "saved_search_id": "ss_1",
            "query": query,
            "notify": notify,
            "status": "saved"
        }
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()