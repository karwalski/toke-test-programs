import urllib.request
import json
import sys

def fetch_json(url):
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode('utf-8'))
    except:
        return {}

def diff_json(obj1, obj2, path=""):
    diffs = []
    
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        all_keys = set(obj1.keys()) | set(obj2.keys())
        for key in sorted(all_keys):
            current_path = f"{path}.{key}" if path else key
            if key not in obj1:
                diffs.append(f"+{current_path}")
            elif key not in obj2:
                diffs.append(f"-{current_path}")
            else:
                sub_diffs = diff_json(obj1[key], obj2[key], current_path)
                diffs.extend(sub_diffs)
    elif isinstance(obj1, list) and isinstance(obj2, list):
        max_len = max(len(obj1), len(obj2))
        for i in range(max_len):
            current_path = f"{path}[{i}]"
            if i >= len(obj1):
                diffs.append(f"+{current_path}")
            elif i >= len(obj2):
                diffs.append(f"-{current_path}")
            else:
                sub_diffs = diff_json(obj1[i], obj2[i], current_path)
                diffs.extend(sub_diffs)
    else:
        if obj1 != obj2:
            diffs.append(f"~{path}")
    
    return diffs

# Read URLs from stdin
url1 = input().strip()
url2 = input().strip()

# Fetch JSON from both URLs
json1 = fetch_json(url1)
json2 = fetch_json(url2)

# Generate diff
diffs = diff_json(json1, json2)

# Print results
if diffs:
    print("~")
else:
    print("~")