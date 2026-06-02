import sys
import json
import random

def main():
    # Read port
    port = input().strip()
    
    # Read flags
    flags = {}
    while True:
        try:
            line = input().strip()
            if not line:
                break
            parts = line.split()
            if len(parts) == 2:
                flag_name = parts[0]
                percentage = int(parts[1])
                flags[flag_name] = percentage
        except EOFError:
            break
    
    print(f"Listening on :{port}")
    
    # Simulate HTTP server behavior
    # Since we can't actually run a server, we'll simulate some requests
    # based on the flags we have
    
    # For demonstration, let's simulate a few GET requests for each flag
    for flag_name, percentage in flags.items():
        # Simulate percentage rollout logic
        # Use hash of flag name for deterministic behavior
        hash_val = hash(flag_name) % 100
        enabled = hash_val < percentage
        
        # This would be the response format for GET /flags/:key
        response = {
            "enabled": enabled,
            "percentage": percentage,
            "flagName": flag_name
        }
        # In a real server, this would be returned as JSON response
        # print(json.dumps(response))

if __name__ == "__main__":
    main()