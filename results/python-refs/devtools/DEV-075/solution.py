import json
import sys

def generate_mock_value(schema):
    """Generate mock data based on JSON schema type"""
    schema_type = schema.get('type')
    
    if schema_type == 'string':
        return "example_string"
    elif schema_type == 'integer':
        return 42
    elif schema_type == 'number':
        return 42.0
    elif schema_type == 'boolean':
        return True
    elif schema_type == 'array':
        items_schema = schema.get('items', {})
        return [generate_mock_value(items_schema)]
    elif schema_type == 'object':
        result = {}
        properties = schema.get('properties', {})
        for prop_name, prop_schema in properties.items():
            result[prop_name] = generate_mock_value(prop_schema)
        return result
    else:
        return None

# Read JSON schema from stdin
input_data = sys.stdin.read().strip()
schema = json.loads(input_data)

# Generate mock data
mock_data = generate_mock_value(schema)

# Output as JSON with sorted keys (to match expected output format)
print(json.dumps(mock_data, separators=(',', ':'), sort_keys=True))