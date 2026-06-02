import json
import sys

# Read input
prefs_line = input().strip()
message_line = input().strip()

# Parse JSON
prefs = json.loads(prefs_line)
message = json.loads(message_line)

# Extract message details
sender = message["sender"]
msg_type = message["type"]
channel = message["channel"]

# Check if channel is muted
if channel in prefs.get("muted", []):
    print("SILENT (reason: channel is muted)")
    sys.exit()

# Check for type-specific sound
if msg_type in prefs.get("types", {}):
    sound = prefs["types"][msg_type]
    print(f"{sound} (reason: type '{msg_type}' overrides contact sound)")
    sys.exit()

# Check for contact-specific sound
if sender in prefs.get("contacts", {}):
    sound = prefs["contacts"][sender]
    print(f"{sound} (reason: contact '{sender}' has custom sound)")
    sys.exit()

# Use default sound
default_sound = prefs.get("default", "ding")
print(f"{default_sound} (reason: using default sound)")