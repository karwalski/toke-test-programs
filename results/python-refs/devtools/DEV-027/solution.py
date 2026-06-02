import json
import sys

def main():
    # Read all input
    input_data = sys.stdin.read().strip()
    
    # Split by separator
    parts = input_data.split('\n---\n')
    if len(parts) != 2:
        return
    
    # Parse JSON specs
    try:
        spec1 = json.loads(parts[0])
        spec2 = json.loads(parts[1])
    except json.JSONDecodeError:
        return
    
    # Extract paths and methods
    paths1 = extract_endpoints(spec1)
    paths2 = extract_endpoints(spec2)
    
    # Find differences
    added = paths2 - paths1
    removed = paths1 - paths2
    
    # Output changes
    for endpoint in sorted(removed):
        method, path = endpoint.split(' ', 1)
        print(f"REMOVED (breaking): {method} {path}")
    
    for endpoint in sorted(added):
        method, path = endpoint.split(' ', 1)
        print(f"ADDED (non-breaking): {method} {path}")

def extract_endpoints(spec):
    endpoints = set()
    if 'paths' in spec:
        for path, methods in spec['paths'].items():
            for method in methods:
                endpoints.add(f"{method.upper()} {path}")
    return endpoints

if __name__ == "__main__":
    main()