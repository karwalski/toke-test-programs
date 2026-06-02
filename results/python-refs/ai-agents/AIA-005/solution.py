import json
import sys

def generate_recovery_strategy(input_data):
    tool_call = input_data["tool_call"]
    error = input_data["error"]
    available_tools = input_data["available_tools"]
    
    error_code = error.get("code", "")
    error_message = error.get("message", "").lower()
    
    # Strategy 1: Retry with modified params for common fixable errors
    if error_code == "LIMIT_EXCEEDED" or "limit" in error_message:
        # Extract limit from error message if possible
        if "max limit is" in error_message:
            try:
                max_limit = int(error_message.split("max limit is ")[1].split()[0])
                modified_call = tool_call.copy()
                modified_call["arguments"] = tool_call["arguments"].copy()
                modified_call["arguments"]["limit"] = max_limit
                return {"strategy": "retry", "action": modified_call}
            except (ValueError, IndexError):
                pass
    
    # Handle other parameter validation errors
    if error_code in ["INVALID_PARAMETER", "PARAMETER_ERROR"] or "parameter" in error_message or "invalid" in error_message:
        # Try to fix common parameter issues
        modified_call = tool_call.copy()
        modified_call["arguments"] = tool_call["arguments"].copy()
        
        # Example fixes based on common patterns
        if "limit" in modified_call["arguments"] and isinstance(modified_call["arguments"]["limit"], int):
            if modified_call["arguments"]["limit"] > 100:
                modified_call["arguments"]["limit"] = 100
                return {"strategy": "retry", "action": modified_call}
    
    # Strategy 2: Try alternative tool
    current_tool = tool_call["tool"]
    for alt_tool in available_tools:
        if alt_tool != current_tool:
            # Check if it's a reasonable alternative
            if (current_tool == "search" and alt_tool == "web_search") or \
               (current_tool == "web_search" and alt_tool == "search") or \
               ("search" in current_tool and "search" in alt_tool):
                alternative_call = tool_call.copy()
                alternative_call["tool"] = alt_tool
                return {"strategy": "alternative", "action": alternative_call}
    
    # Strategy 3: Report failure
    return {"strategy": "fail", "action": {"error": f"Unable to recover from {error_code}: {error.get('message', 'Unknown error')}"}}

# Read input from stdin
input_json = sys.stdin.read().strip()
input_data = json.loads(input_json)

# Generate recovery strategy
result = generate_recovery_strategy(input_data)

# Output result to stdout
print(json.dumps(result, separators=(',', ':')))