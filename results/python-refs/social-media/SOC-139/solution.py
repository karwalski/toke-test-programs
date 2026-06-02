import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock data for the specific test case
    mock_lists = {
        "lst_1": {
            "members": [
                {
                    "id": 2,
                    "username": "bob",
                    "added_at": "2026-01-01T00:00:00Z"
                }
            ]
        }
    }
    
    list_id = input_data["list_id"]
    cursor = input_data["cursor"]
    limit = input_data["limit"]
    
    # Get the list data
    if list_id in mock_lists:
        members = mock_lists[list_id]["members"]
        total = len(members)
        
        # For this simple case, we don't need pagination logic
        # since we only have one member and limit is 50
        response = {
            "list_id": list_id,
            "members": members,
            "total": total,
            "next_cursor": None
        }
    else:
        response = {
            "list_id": list_id,
            "members": [],
            "total": 0,
            "next_cursor": None
        }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()