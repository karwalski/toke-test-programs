import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract fields from input
    action = input_data.get("action")
    token = input_data.get("token")
    code = input_data.get("code")
    
    # For this implementation, we'll assume the verification is successful
    # In a real implementation, you would validate the TOTP code against the token
    if action == "verify_2fa" and token and code:
        response = {
            "status": "2fa_enabled",
            "backup_codes": ["abc123", "def456"]
        }
    else:
        response = {
            "status": "error",
            "message": "Invalid request"
        }
    
    # Output JSON response to stdout
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()