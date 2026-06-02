import sys
import json
import re

def parse_parquet_schema(schema_text):
    # Remove the outer message schema { ... } wrapper
    schema_text = schema_text.strip()
    
    # Find content between the braces
    match = re.search(r'message\s+schema\s*\{(.*)\}', schema_text, re.DOTALL)
    if not match:
        return []
    
    content = match.group(1).strip()
    
    # Split by semicolons and process each field
    fields = []
    for line in content.split(';'):
        line = line.strip()
        if not line:
            continue
            
        # Parse field definition: (required|optional) type name [(annotation)];
        field_match = re.match(r'(required|optional)\s+(\w+)\s+(\w+)(?:\s*\((\w+)\))?', line)
        if field_match:
            required_str, field_type, field_name, annotation = field_match.groups()
            
            # Determine if required
            required = required_str == 'required'
            
            # Determine type - use annotation if present, otherwise use field_type
            if annotation:
                type_name = annotation
            else:
                # Map Parquet primitive types to uppercase
                type_map = {
                    'binary': 'BINARY',
                    'int64': 'INT64',
                    'float': 'FLOAT',
                    'double': 'DOUBLE',
                    'boolean': 'BOOLEAN',
                    'int32': 'INT32'
                }
                type_name = type_map.get(field_type, field_type.upper())
            
            fields.append({
                "name": field_name,
                "type": type_name,
                "required": required
            })
    
    return fields

# Read from stdin
input_text = sys.stdin.read()

# Parse the schema
fields = parse_parquet_schema(input_text)

# Output JSON
print(json.dumps(fields, separators=(',', ':')))