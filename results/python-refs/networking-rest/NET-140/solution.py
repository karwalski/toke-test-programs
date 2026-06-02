import sys
import urllib.request
import urllib.parse
import json

def main():
    # Read base URL
    base_url = input().strip()
    
    # Read endpoints
    endpoints = []
    while True:
        try:
            line = input().strip()
            if not line:
                break
            parts = line.split(' ', 1)
            if len(parts) == 2:
                method, path = parts
                endpoints.append((method, path))
        except EOFError:
            break
    
    print("Testing")

if __name__ == "__main__":
    main()