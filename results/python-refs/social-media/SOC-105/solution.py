import json
import sys

def apply_moderation_decision(request):
    report_id = request["report_id"]
    decision = request["decision"]
    reason = request["reason"]
    
    response = {
        "report_id": report_id,
        "decision": decision,
        "post_removed": False,
        "user_warned": False,
        "status": "resolved"
    }
    
    if decision == "remove":
        response["post_removed"] = True
        response["user_warned"] = True
    elif decision == "warn":
        response["user_warned"] = True
    elif decision == "dismiss":
        response["status"] = "dismissed"
    
    return response

# Read input from stdin
input_data = sys.stdin.read().strip()
request = json.loads(input_data)

# Process the moderation decision
result = apply_moderation_decision(request)

# Output JSON response
print(json.dumps(result, separators=(',', ':')))