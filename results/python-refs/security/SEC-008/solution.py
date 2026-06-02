import json
import sys

# Read all input
input_text = sys.stdin.read().strip()

# Split by blank line to separate policy and request
parts = input_text.split('\n\n')
policy_text = parts[0]
request_text = parts[1]

# Parse JSON
policy = json.loads(policy_text)
request = json.loads(request_text)

# Extract data
roles = policy.get('roles', {})
permissions = policy.get('permissions', {})
assignments = policy.get('assignments', {})

user = request['user']
action = request['action']
resource = request['resource']

# Check if user has required permission
user_roles = assignments.get(user, [])
user_permissions = []

# Collect all permissions from user's roles
for role in user_roles:
    if role in roles:
        user_permissions.extend(roles[role])

# Check if user has the required action permission
if action in user_permissions:
    print("PERMIT")
else:
    print("DENY")