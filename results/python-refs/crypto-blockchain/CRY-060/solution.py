import json
import hashlib
import sys

# Read input
setup_line = input().strip()
action_line = input().strip()
current_time = int(input().strip())

# Parse setup parameters
setup = json.loads(setup_line)
sender = setup["sender"]
receiver = setup["receiver"]
amount = setup["amount"]
hashlock = setup["hashlock"]
timelock = setup["timelock"]

# Parse action
action_parts = action_line.split(" ", 1)
action_type = action_parts[0]

if action_type == "claim":
    if len(action_parts) < 2:
        print("FAILED: No preimage provided")
        sys.exit()
    
    preimage = action_parts[1]
    
    # Check if timelock has expired
    if current_time >= timelock:
        print("FAILED: Timelock expired")
        sys.exit()
    
    # Verify preimage hash matches hashlock
    preimage_hash = hashlib.sha256(preimage.encode()).hexdigest()
    
    if preimage_hash == hashlock:
        print(f"SUCCESS: {receiver} receives {amount}")
    else:
        print("FAILED: Invalid preimage")

elif action_type == "refund":
    # Check if timelock has expired
    if current_time >= timelock:
        print(f"SUCCESS: {sender} receives {amount}")
    else:
        print("FAILED: Timelock not yet expired")

else:
    print("FAILED: Invalid action")