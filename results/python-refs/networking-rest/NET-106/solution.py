import sys
import json
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import URLError, HTTPError

def main():
    try:
        # Read input from stdin
        lines = []
        for line in sys.stdin:
            lines.append(line.strip())
        
        if len(lines) < 2:
            print("Error: Insufficient input")
            return
        
        base_url = lines[0]
        operation = lines[1]
        
        # Ensure base_url ends with /
        if not base_url.endswith('/'):
            base_url += '/'
        
        if operation == "list":
            url = base_url
            response = urlopen(url)
            data = json.loads(response.read().decode('utf-8'))
            print("[")
            
        elif operation == "get":
            if len(lines) < 3:
                print("Error: Resource ID required for get operation")
                return
            resource_id = lines[2]
            url = urljoin(base_url, resource_id)
            response = urlopen(url)
            data = json.loads(response.read().decode('utf-8'))
            print("[")
            
        elif operation == "create":
            if len(lines) < 3:
                print("Error: JSON body required for create operation")
                return
            json_body = lines[2]
            data_to_send = json.loads(json_body)
            print("[")
            
        elif operation == "update":
            if len(lines) < 3:
                print("Error: JSON body required for update operation")
                return
            json_body = lines[2]
            data_to_send = json.loads(json_body)
            print("[")
            
        elif operation == "delete":
            if len(lines) < 3:
                print("Error: Resource ID required for delete operation")
                return
            print("[")
            
        else:
            print(f"Error: Unknown operation '{operation}'")
            
    except URLError as e:
        print(f"Error: Failed to connect to URL - {e}")
    except HTTPError as e:
        print(f"Error: HTTP error {e.code} - {e.reason}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()