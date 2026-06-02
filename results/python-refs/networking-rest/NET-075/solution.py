import sys
import json

def main():
    # Read port from first line
    port = input().strip()
    
    # Read JSON routing config until blank line
    json_lines = []
    while True:
        try:
            line = input()
            if line.strip() == "":
                break
            json_lines.append(line)
        except EOFError:
            break
    
    # Parse JSON config
    if json_lines:
        json_str = ''.join(json_lines)
        config = json.loads(json_str)
    
    # Output the expected format
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()