import json
import sys

input_data = sys.stdin.read().strip()
request = json.loads(input_data)

if request.get("action") == "delete_post":
    post_id = request.get("post_id")
    print(json.dumps({"post_id": post_id, "status": "deleted"}, separators=(',', ':')))
else:
    print(json.dumps({"error": "Invalid action"}, separators=(',', ':')))