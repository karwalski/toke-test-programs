import sys
import re

def extract_types_and_interfaces(file_path):
    try:
        with open(file_path.strip(), 'r') as file:
            content = file.read()
    except FileNotFoundError:
        return
    
    # Remove comments and strings to avoid false matches
    content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    content = re.sub(r'"[^"]*"', '""', content)
    content = re.sub(r"'[^']*'", "''", content)
    content = re.sub(r'`[^`]*`', '``', content)
    
    # Pattern to match interface or type definitions
    pattern = r'(interface|type)\s+(\w+)\s*\{([^}]*)\}'
    
    matches = re.findall(pattern, content, re.DOTALL)
    
    for match in matches:
        keyword, name, body = match
        print(f"{keyword} {name} {{")
        
        # Extract field definitions
        fields = []
        lines = body.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            # Remove trailing comma and semicolon
            line = line.rstrip(',;')
            
            # Match field patterns like "fieldName: type" or "fieldName?: type"
            field_match = re.match(r'^\s*(\w+)\s*\??\s*:\s*([^,;]+)', line)
            if field_match:
                field_name = field_match.group(1)
                field_type = field_match.group(2).strip()
                fields.append(f"  {field_name}: {field_type}")
        
        for field in fields:
            print(field)
        
        print("}")

# Read input from stdin
file_path = input()
extract_types_and_interfaces(file_path)