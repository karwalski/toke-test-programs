import json
import sys
import hashlib

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    request = json.loads(input_data)
    
    action = request.get("action")
    token = request.get("token")
    folder_name = request.get("folder_name")
    
    # Simple token validation (just check if it exists)
    if not token:
        response = {"error": "Invalid token"}
        print(json.dumps(response, separators=(',', ':')))
        return
    
    if action == "create_bookmark_folder":
        # Generate a simple folder ID
        folder_id = "bf_1"
        
        response = {
            "folder_id": folder_id,
            "name": folder_name,
            "post_count": 0,
            "status": "created"
        }
        
        print(json.dumps(response, separators=(',', ':')))
    
    elif action == "list_bookmark_folders":
        # Return empty list or sample folders
        response = {
            "folders": [],
            "status": "success"
        }
        
        print(json.dumps(response, separators=(',', ':')))
    
    else:
        response = {"error": "Unknown action"}
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()