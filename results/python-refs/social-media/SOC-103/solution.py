import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock notifications database
    notifications = [
        {"id": "n1", "actor": "alice", "post_id": 5, "created_at": "2025-12-31T23:00:00Z", "type": "like"},
        {"id": "n2", "actor": "bob", "post_id": 8, "created_at": "2025-12-31T23:30:00Z", "type": "comment"},
        {"id": "n3", "actor": "alice", "post_id": 12, "created_at": "2026-01-01T00:00:00Z", "type": "like"},
        {"id": "n4", "actor": "david", "post_id": 15, "created_at": "2026-01-01T00:30:00Z", "type": "follow"},
        {"id": "n5", "actor": "carol", "post_id": 10, "created_at": "2026-01-01T00:00:00Z", "type": "mentions"}
    ]
    
    # Extract parameters
    action = input_data.get("action")
    token = input_data.get("token")
    notification_type = input_data.get("type")
    cursor = input_data.get("cursor")
    
    # Filter notifications by type
    filtered_notifications = []
    for notification in notifications:
        if notification.get("type") == notification_type:
            # Remove the type field from the notification object for output
            filtered_notification = {k: v for k, v in notification.items() if k != "type"}
            filtered_notifications.append(filtered_notification)
    
    # Create response
    response = {
        "type": notification_type,
        "notifications": filtered_notifications,
        "next_cursor": None
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()