import sys
import yaml

def parse_input():
    content = sys.stdin.read().strip()
    parts = content.split('\n\n')
    
    if len(parts) != 2:
        return {}, {}
    
    try:
        file_a = yaml.safe_load(parts[0]) or {}
        file_b = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}, {}
    
    return file_a, file_b

def diff_configs(file_a, file_b):
    changes = []
    
    # Find all unique keys
    all_keys = set(file_a.keys()) | set(file_b.keys())
    
    for key in sorted(all_keys):
        if key in file_a and key in file_b:
            if file_a[key] != file_b[key]:
                changes.append(f"~ {key}: {file_a[key]} -> {file_b[key]}")
        elif key in file_a and key not in file_b:
            changes.append(f"- {key}: {file_a[key]}")
        elif key not in file_a and key in file_b:
            changes.append(f"+ {key}: {file_b[key]}")
    
    return changes

def main():
    file_a, file_b = parse_input()
    changes = diff_configs(file_a, file_b)
    
    for change in changes:
        print(change)

if __name__ == "__main__":
    main()