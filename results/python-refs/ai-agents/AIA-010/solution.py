import json
import sys

def check_permission(input_data):
    user_role = input_data["user_role"]
    tool_call = input_data["tool_call"]
    permissions = input_data["permissions"]
    
    tool_name = tool_call["tool"]
    
    # Check if user role exists in permissions
    if user_role not in permissions:
        return {
            "allowed": False,
            "reason": f"Role {user_role} not found in permissions"
        }
    
    user_permissions = permissions[user_role]
    
    # Check if user has wildcard permission
    if "*" in user_permissions:
        return {
            "allowed": True,
            "reason": f"Role {user_role} has wildcard permission"
        }
    
    # Check if user has specific tool permission
    if tool_name in user_permissions:
        return {
            "allowed": True,
            "reason": f"Role {user_role} has permission for {tool_name}"
        }
    
    # Permission denied
    return {
        "allowed": False,
        "reason": f"Role {user_role} does not have permission for {tool_name}"
    }

# Read input from stdin
input_text = sys.stdin.read().strip()
input_data = json.loads(input_text)

# Check permission
result = check_permission(input_data)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))