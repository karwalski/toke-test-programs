import json
import sys
from collections import defaultdict

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock notification data - in a real system this would come from a database
    notifications = [
        {"type": "like", "post_id": 1, "actor": "bob", "timestamp": "2026-01-01T01:00:00Z"},
        {"type": "like", "post_id": 1, "actor": "carol", "timestamp": "2026-01-01T02:00:00Z"},
        {"type": "like", "post_id": 1, "actor": "dave", "timestamp": "2026-01-01T03:00:00Z"},
    ]
    
    # Group notifications by type and post_id
    groups = defaultdict(lambda: {"actors": [], "timestamps": []})
    
    for notification in notifications:
        key = (notification["type"], notification["post_id"])
        groups[key]["actors"].append(notification["actor"])
        groups[key]["timestamps"].append(notification["timestamp"])
    
    # Build grouped notifications response
    grouped_notifications = []
    for (notification_type, post_id), data in groups.items():
        # Sort timestamps to get the latest one
        data["timestamps"].sort()
        latest_timestamp = data["timestamps"][-1]
        
        grouped_notification = {
            "type": notification_type,
            "post_id": post_id,
            "actors": data["actors"],
            "count": len(data["actors"]),
            "latest_at": latest_timestamp
        }
        grouped_notifications.append(grouped_notification)
    
    # Create response
    response = {
        "groups": grouped_notifications,
        "next_cursor": None
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()