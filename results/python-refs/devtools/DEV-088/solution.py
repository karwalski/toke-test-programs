import sys
import re

def parse_graphql_schema(schema_text):
    # Remove comments and normalize whitespace
    lines = []
    for line in schema_text.split('\n'):
        # Remove comments
        if '#' in line:
            line = line[:line.index('#')]
        line = line.strip()
        if line:
            lines.append(line)
    
    text = ' '.join(lines)
    
    # Find all type definitions
    type_pattern = r'type\s+(\w+)\s*\{([^}]*)\}'
    types = {}
    
    for match in re.finditer(type_pattern, text):
        type_name = match.group(1)
        fields_text = match.group(2)
        
        # Parse fields
        fields = []
        # Split by potential field separators and clean up
        field_parts = re.split(r'[,\n]', fields_text)
        
        for field_part in field_parts:
            field_part = field_part.strip()
            if not field_part:
                continue
                
            # Match field pattern: fieldName(args...): Type
            field_match = re.match(r'(\w+)(\([^)]*\))?\s*:\s*(.+)', field_part)
            if field_match:
                field_name = field_match.group(1)
                field_type = field_match.group(3).strip()
                fields.append((field_name, field_type))
        
        types[type_name] = fields
    
    return types

def main():
    schema_text = sys.stdin.read()
    types = parse_graphql_schema(schema_text)
    
    # Sort types to ensure consistent output (Query first if present, then alphabetical)
    sorted_types = []
    if 'Query' in types:
        sorted_types.append('Query')
    for type_name in sorted(types.keys()):
        if type_name != 'Query':
            sorted_types.append(type_name)
    
    for i, type_name in enumerate(sorted_types):
        if i > 0:
            print()  # Empty line between types
        print(f"{type_name}:")
        for field_name, field_type in types[type_name]:
            print(f"  {field_name}: {field_type}")

if __name__ == "__main__":
    main()