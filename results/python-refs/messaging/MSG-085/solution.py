import json
import re
import sys

# Read input
policy_line = input().strip()
message_type = input().strip()
message_content = input().strip()

# Parse policy
policy = json.loads(policy_line)
max_length = policy["max_length"]
allowed_types = policy["allowed_types"]
prohibited_patterns = policy["prohibited_patterns"]

# Check violations
violations = []

# Check message type
if message_type not in allowed_types:
    violations.append(f"disallowed type: {message_type}")

# Check max length
if len(message_content) > max_length:
    violations.append(f"exceeds max length: {len(message_content)}")

# Check prohibited patterns
for pattern in prohibited_patterns:
    if re.search(pattern, message_content, re.IGNORECASE):
        # Extract the matched word for output
        match = re.search(pattern, message_content, re.IGNORECASE)
        matched_word = match.group().lower()
        violations.append(f"prohibited pattern match: {matched_word}")

# Output result
if violations:
    print("REJECTED")
    for violation in violations:
        print(f"- {violation}")
else:
    print("ALLOWED")