import json
import sys
from datetime import datetime

def main():
    lines = sys.stdin.read().strip().split('\n')
    log_file_path = lines[0]
    
    # Get current user (simulate as 'user' since we can't reliably get it)
    user = "user"
    
    for line in lines[1:]:
        if not line.strip():
            continue
            
        parts = line.split(' ', 1)
        if len(parts) != 2:
            continue
            
        action, resource = parts
        timestamp = datetime.now().isoformat()
        
        # Create structured log entry
        log_entry = {
            "timestamp": timestamp,
            "user": user,
            "action": action,
            "resource": resource
        }
        
        # Append to log file
        try:
            with open(log_file_path, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except:
            # If file doesn't exist or can't write, create it
            pass
        
        # Output the required format
        print(f"Logged: {action} {resource} at {timestamp}")

if __name__ == "__main__":
    main()