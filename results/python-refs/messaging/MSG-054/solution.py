import json
import sys

# Read routing rules from first line
rules_line = input().strip()
routing_rules = json.loads(rules_line)

# Process each message
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    message = json.loads(line)
    routed_channels = []
    
    # Check each routing rule
    for rule in routing_rules:
        channel = rule["channel"]
        rules = rule["rules"]
        
        # Check if message matches this rule
        matches = True
        
        # Check keywords
        if rules["keywords"]:
            keyword_match = False
            message_text = message.get("text", "").lower()
            for keyword in rules["keywords"]:
                if keyword.lower() in message_text:
                    keyword_match = True
                    break
            if not keyword_match:
                matches = False
        
        # Check senders
        if rules["senders"]:
            if message.get("sender") not in rules["senders"]:
                matches = False
        
        # Check types
        if rules["types"]:
            if message.get("type") not in rules["types"]:
                matches = False
        
        # If all conditions match, route to this channel
        if matches:
            routed_channels.append(channel)
    
    # Output result
    if routed_channels:
        print("routed to: " + ", ".join(routed_channels))
    else:
        print("routed to: ")