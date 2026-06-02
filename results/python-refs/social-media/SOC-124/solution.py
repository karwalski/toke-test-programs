import json
import sys

def get_personalized_trends(token, limit):
    # Mock personalized trends based on token
    # In a real system, this would analyze user's past engagement and interests
    trends = [
        {
            "topic": "systems programming",
            "relevance_score": 0.92,
            "reason": "matches_interests",
            "post_count": 500
        }
    ]
    
    return trends[:limit]

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    action = input_data.get("action")
    token = input_data.get("token")
    limit = input_data.get("limit", 10)
    
    if action == "personalized_trends":
        trends = get_personalized_trends(token, limit)
        response = {"trends": trends}
        print(json.dumps(response, separators=(',', ':')))
    else:
        response = {"error": "Invalid action"}
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()