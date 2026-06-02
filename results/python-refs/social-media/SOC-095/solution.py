import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    action = input_data.get("action")
    token = input_data.get("token")
    notification_id = input_data.get("notification_id")
    mark_all = input_data.get("mark_all")
    
    if action == "mark_read":
        if notification_id:
            # Mark single notification as read
            response = {
                "notification_id": notification_id,
                "read": True,
                "status": "marked_read"
            }
        elif mark_all:
            # Mark all notifications as read
            response = {
                "read": True,
                "status": "all_marked_read"
            }
        else:
            response = {
                "error": "notification_id or mark_all required"
            }
    else:
        response = {
            "error": "invalid action"
        }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()