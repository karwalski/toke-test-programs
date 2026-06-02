import json
import sys

# Read input
platform = input().strip()
message_json = input().strip()
message = json.loads(message_json)

if platform == "ios":
    # Construct APNs payload
    payload = {
        "aps": {
            "alert": {
                "title": message["sender"],
                "body": message["text"]
            },
            "badge": message["badge_count"],
            "sound": message["sound"]
        }
    }
elif platform == "android":
    # Construct FCM payload
    payload = {
        "notification": {
            "title": message["sender"],
            "body": message["text"],
            "sound": message["sound"]
        },
        "data": {
            "badge_count": str(message["badge_count"])
        }
    }

# Output JSON without spaces
print(json.dumps(payload, separators=(',', ':')))