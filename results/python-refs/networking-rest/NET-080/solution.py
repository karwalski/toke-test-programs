import sys
import json

def main():
    lines = sys.stdin.read().strip().split('\n')
    port = lines[0]
    
    # Join remaining lines to get the OpenAPI spec
    openapi_json = '\n'.join(lines[1:])
    
    try:
        spec = json.loads(openapi_json)
    except json.JSONDecodeError:
        spec = {}
    
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()