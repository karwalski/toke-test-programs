import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

query = input_data['query']
tool_name = input_data['tool_name']
result = input_data['result']

# Format the response based on tool type
if tool_name == 'weather':
    temp = result['temp_c']
    condition = result['condition']
    humidity = result['humidity']
    
    # Extract location from query (assuming "What is the weather in [location]?" format)
    location = query.split(' in ')[-1].rstrip('?')
    
    response = f"The weather in {location} is currently {temp}°C and {condition} with {humidity}% humidity."
    
print(response)