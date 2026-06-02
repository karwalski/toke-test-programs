import json
import sys
from datetime import datetime

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    action = input_data.get("action")
    token = input_data.get("token")
    
    if action == "list_sessions":
        # Mock session data for demonstration
        sessions = [
            {
                "id": "s1",
                "device": "Chrome/Mac",
                "created_at": "2026-01-01T00:00:00Z",
                "current": True
            }
        ]
        
        response = {"sessions": sessions}
        
    elif action == "revoke_session":
        session_id = input_data.get("session_id")
        # Mock revoke response
        response = {"success": True, "message": f"Session {session_id} revoked"}
        
    else:
        response = {"error": "Invalid action"}
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()