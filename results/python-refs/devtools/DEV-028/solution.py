import json
import sys

def compare_schemas(schema1, schema2):
    def get_fields(schema):
        fields = {}
        if 'properties' in schema:
            for field_name, field_def in schema['properties'].items():
                if 'type' in field_def:
                    fields[field_name] = field_def['type']
        return fields
    
    fields1 = get_fields(schema1)
    fields2 = get_fields(schema2)
    
    results = []
    
    # Check for removed fields
    for field in fields1:
        if field not in fields2:
            results.append(f"REMOVED: {field}")
    
    # Check for added fields
    for field in fields2:
        if field not in fields1:
            results.append(f"ADDED: {field}")
    
    # Check for changed fields
    for field in fields1:
        if field in fields2 and fields1[field] != fields2[field]:
            results.append(f"CHANGED: {field} ({fields1[field]}->{fields2[field]})")
    
    return results

# Read input from stdin
input_text = sys.stdin.read().strip()

# Split on '---'
parts = input_text.split('---')
schema1_text = parts[0].strip()
schema2_text = parts[1].strip()

# Parse JSON schemas
schema1 = json.loads(schema1_text)
schema2 = json.loads(schema2_text)

# Compare schemas
differences = compare_schemas(schema1, schema2)

# Output results
for diff in differences:
    print(diff)