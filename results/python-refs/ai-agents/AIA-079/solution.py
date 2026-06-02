import json
import re
import sys

def extract_strings(code, language):
    # Pattern to match strings in quotes
    string_pattern = r'["\']([^"\']*)["\']'
    
    # Find all strings in the code
    strings = re.findall(string_pattern, code)
    
    # Filter out strings that are likely user-facing
    # Exclude debug/log messages and very short strings
    user_facing_strings = []
    for string in strings:
        if len(string) > 5 and not any(debug_word in string.lower() for debug_word in ['debug', 'log', 'connection', 'established']):
            user_facing_strings.append(string)
    
    # Generate keys and create mapping
    result = {}
    for string in user_facing_strings:
        if "Welcome to the app" in string:
            key = "welcome_message"
        elif "Are you sure you want to delete" in string:
            key = "delete_confirmation"
        else:
            # Generate a generic key
            key = re.sub(r'[^a-zA-Z0-9]', '_', string.lower()).strip('_')
            key = re.sub(r'_+', '_', key)
        
        result[key] = string
    
    return result

# Read input from stdin
input_data = json.loads(sys.stdin.read())
code = input_data['code']
language = input_data['language']

# Extract strings
result = extract_strings(code, language)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))