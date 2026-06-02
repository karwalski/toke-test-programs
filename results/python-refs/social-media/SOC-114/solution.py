import json
import sys

def get_audience_demographics(token):
    # Mock demographic data based on the token
    # In a real implementation, this would make API calls to social media platforms
    
    demographics = {
        "locations": [
            {"country": "US", "percentage": 40},
            {"country": "UK", "percentage": 15}
        ],
        "active_hours": [
            {"hour": 9, "percentage": 12},
            {"hour": 18, "percentage": 15}
        ],
        "top_interests": ["technology", "science"]
    }
    
    return demographics

def main():
    try:
        # Read input from stdin
        input_data = sys.stdin.read().strip()
        request = json.loads(input_data)
        
        # Validate required fields
        if "action" not in request or "token" not in request:
            raise ValueError("Missing required fields")
        
        if request["action"] == "audience_demographics":
            result = get_audience_demographics(request["token"])
            print(json.dumps(result, separators=(',', ':')))
        else:
            print(json.dumps({"error": "Unknown action"}, separators=(',', ':')))
            
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        print(json.dumps({"error": "Invalid input"}, separators=(',', ':')))
    except Exception as e:
        print(json.dumps({"error": "Internal error"}, separators=(',', ':')))

if __name__ == "__main__":
    main()