import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()

try:
    # Parse JSON
    metadata = json.loads(input_data)
    
    # Check required fields
    required_fields = ["name", "description", "image"]
    
    for field in required_fields:
        if field not in metadata:
            print(f"INVALID: missing {field}")
            sys.exit()
    
    # If all required fields are present
    print("VALID")
    
    # Get values
    name = metadata["name"]
    description = metadata["description"]
    image = metadata["image"]
    
    # Truncate description to first 50 chars if needed
    if len(description) > 50:
        description = description[:50]
    
    # Output summary
    print(f"{name} | {description} | {image}")
    
except json.JSONDecodeError:
    print("INVALID: invalid JSON")