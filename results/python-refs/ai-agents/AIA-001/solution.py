import json
import sys
import re

def parse_query_and_dispatch():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())
    tools = input_data['tools']
    query = input_data['query'].lower()
    
    # Simple keyword matching for tool selection
    selected_tool = None
    arguments = {}
    
    for tool in tools:
        tool_name = tool['name']
        params = tool['params']
        
        # Check if tool name is mentioned in query
        if tool_name in query:
            selected_tool = tool_name
            
            # Extract arguments based on parameters
            for param in params:
                if param == 'city':
                    # Look for city names after "in" or "for"
                    city_match = re.search(r'\b(?:in|for)\s+([A-Za-z\s]+?)(?:\?|$|\.)', query)
                    if city_match:
                        arguments[param] = city_match.group(1).strip().title()
                elif param == 'date':
                    # Look for date patterns
                    date_match = re.search(r'\b(?:on|for)\s+([A-Za-z0-9\s\-/,]+?)(?:\?|$|\.)', query)
                    if date_match:
                        arguments[param] = date_match.group(1).strip()
            break
    
    # Output result
    result = {
        "tool": selected_tool,
        "arguments": arguments
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    parse_query_and_dispatch()