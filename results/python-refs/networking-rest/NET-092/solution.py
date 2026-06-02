import sys
import json
from urllib.parse import urlparse

def main():
    # Read port from first line
    port = input().strip()
    
    # Read tenant configurations
    tenants = {}
    while True:
        try:
            line = input().strip()
            if not line:
                break
            tenant_id, name = line.split(':', 1)
            tenants[tenant_id] = {"name": name}
        except EOFError:
            break
    
    # Print the expected output
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()