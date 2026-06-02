import json
import sys

def get_unread_notifications(token):
    # Mock data for demonstration - in a real app this would query a database
    notifications = [
        {"type": "likes", "read": False},
        {"type": "likes", "read": False},
        {"type": "comments", "read": False},
        {"type": "follows", "read": False},
        {"type": "mentions", "read": False},
        {"type": "likes", "read": True},
        {"type": "comments", "read": True}
    ]
    
    # Count unread notifications by type
    breakdown = {}
    total = 0
    
    for notification in notifications:
        if not notification["read"]:
            notification_type = notification["type"]
            breakdown[notification_type] = breakdown.get(notification_type, 0) + 1
            total += 1
    
    return {"total": total, "breakdown": breakdown}

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Validate input
if input_data.get("action") == "unread_count" and "token" in input_data:
    result = get_unread_notifications(input_data["token"])
    print(json.dumps(result, separators=(',', ':')))
else:
    print(json.dumps({"error": "Invalid request"}, separators=(',', ':')))