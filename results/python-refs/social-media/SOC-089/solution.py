import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    clear_all = input_data.get("clear_all")
    query_id = input_data.get("query_id")
    
    # Process the clear searches action
    if action == "clear_searches" and token:
        if clear_all:
            # Clear all search history
            response = {
                "cleared": True,
                "status": "search_history_cleared"
            }
        elif query_id:
            # Clear specific query
            response = {
                "cleared": True,
                "status": "query_removed"
            }
        else:
            response = {
                "cleared": False,
                "status": "invalid_request"
            }
    else:
        response = {
            "cleared": False,
            "status": "invalid_request"
        }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()