import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    report_id = input_data.get("report_id")
    appeal_text = input_data.get("appeal_text")
    
    # Validate the action
    if action != "appeal":
        response = {"error": "Invalid action"}
    else:
        # Generate appeal response
        response = {
            "appeal_id": "app_001",
            "report_id": report_id,
            "status": "under_review",
            "estimated_response_hours": 48
        }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()