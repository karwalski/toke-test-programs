import json
import sys

def deduplicate_tool_calls(tool_calls):
    unique_calls = []
    duplicates = []
    seen = set()
    
    for call in tool_calls:
        # Create a key for deduplication based on tool and arguments
        key = (call['tool'], json.dumps(call['arguments'], sort_keys=True))
        
        if key not in seen:
            seen.add(key)
            unique_calls.append(call)
        else:
            duplicates.append(call['id'])
    
    return {
        "unique_calls": unique_calls,
        "duplicates": duplicates
    }

# Read input from stdin
input_data = sys.stdin.read().strip()
tool_calls = json.loads(input_data)

# Process the tool calls
result = deduplicate_tool_calls(tool_calls)

# Output the result as JSON
print(json.dumps(result, separators=(',', ':')))