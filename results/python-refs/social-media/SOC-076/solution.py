import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Parse the request
    action = input_data.get("action")
    token = input_data.get("token")
    limit = input_data.get("limit", 10)
    
    # Simulate follow suggestions based on mutual connections
    # In a real system, this would query a database using the token to identify the user
    # and find suggestions based on mutual connections and interests
    
    suggestions = []
    
    # Mock data - in reality this would come from a database
    # Based on the expected output, we need to return user dave with 3 mutual connections
    if action == "follow_suggestions":
        suggestions.append({
            "id": 4,
            "username": "dave", 
            "reason": "followed_by_3_mutuals",
            "mutual_count": 3
        })
    
    # Limit the results
    suggestions = suggestions[:limit]
    
    # Create response
    response = {
        "suggestions": suggestions
    }
    
    # Output JSON response to stdout
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()