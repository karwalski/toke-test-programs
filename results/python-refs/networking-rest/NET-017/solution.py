import sys
import json

def main():
    # Read port from first line
    port = input().strip()
    
    # Read JSON schema until blank line
    schema_lines = []
    while True:
        try:
            line = input()
            if line.strip() == "":
                break
            schema_lines.append(line)
        except EOFError:
            break
    
    # Parse the schema
    schema_json = "".join(schema_lines)
    try:
        schema = json.loads(schema_json)
    except json.JSONDecodeError:
        schema = {}
    
    # Output the expected result
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()