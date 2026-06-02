import sys
import json
import urllib.request
import urllib.parse
import copy

def apply_json_patch(doc, patch):
    """Apply JSON Patch operations to a document"""
    result = copy.deepcopy(doc)
    
    for operation in patch:
        op = operation["op"]
        path = operation["path"]
        
        if op == "replace":
            value = operation["value"]
            path_parts = path.strip("/").split("/") if path != "/" else []
            
            if not path_parts:
                result = value
            else:
                current = result
                for part in path_parts[:-1]:
                    if part.isdigit():
                        current = current[int(part)]
                    else:
                        current = current[part]
                
                last_part = path_parts[-1]
                if last_part.isdigit():
                    current[int(last_part)] = value
                else:
                    current[last_part] = value
        
        elif op == "add":
            value = operation["value"]
            path_parts = path.strip("/").split("/") if path != "/" else []
            
            if not path_parts:
                result = value
            else:
                current = result
                for part in path_parts[:-1]:
                    if part.isdigit():
                        current = current[int(part)]
                    else:
                        current = current[part]
                
                last_part = path_parts[-1]
                if isinstance(current, list):
                    if last_part == "-":
                        current.append(value)
                    else:
                        current.insert(int(last_part), value)
                else:
                    current[last_part] = value
        
        elif op == "remove":
            path_parts = path.strip("/").split("/") if path != "/" else []
            
            if path_parts:
                current = result
                for part in path_parts[:-1]:
                    if part.isdigit():
                        current = current[int(part)]
                    else:
                        current = current[part]
                
                last_part = path_parts[-1]
                if isinstance(current, list):
                    current.pop(int(last_part))
                else:
                    del current[last_part]
    
    return result

def main():
    lines = sys.stdin.read().strip().split('\n')
    url = lines[0]
    patch_json = '\n'.join(lines[1:])
    
    # Parse the JSON patch
    patch = json.loads(patch_json)
    
    # Fetch current resource
    with urllib.request.urlopen(url) as response:
        original_doc = json.loads(response.read().decode())
    
    # Apply patch locally to validate
    patched_doc = apply_json_patch(original_doc, patch)
    
    # Send HTTP PATCH request
    patch_data = json.dumps(patched_doc).encode()
    req = urllib.request.Request(url, data=patch_data, method='PATCH')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            print(status_code)
    except urllib.error.HTTPError as e:
        print(e.code)

if __name__ == "__main__":
    main()