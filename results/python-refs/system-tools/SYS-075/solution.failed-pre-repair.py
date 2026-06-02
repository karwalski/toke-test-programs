import json
import configparser
import sys

def read_config_file(filepath):
    """Read a config file and return a dictionary of key-value pairs."""
    try:
        # Try to read as JSON first
        with open(filepath, 'r') as f:
            content = f.read().strip()
            if content.startswith('{') or content.startswith('['):
                return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        pass
    
    try:
        # Try to read as INI file
        config = configparser.ConfigParser()
        config.read(filepath)
        result = {}
        for section in config.sections():
            for key, value in config.items(section):
                # Use section.key format for INI files
                result[f"{section}.{key}"] = value
        return result
    except:
        pass
    
    return {}

def flatten_dict(d, parent_key='', sep='.'):
    """Flatten a nested dictionary."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def compare_configs(file1_path, file2_path):
    """Compare two config files and return differences."""
    config1 = read_config_file(file1_path)
    config2 = read_config_file(file2_path)
    
    # Flatten nested dictionaries
    flat1 = flatten_dict(config1)
    flat2 = flatten_dict(config2)
    
    differences = []
    
    # Find added keys (in file2 but not in file1)
    for key in flat2:
        if key not in flat1:
            differences.append(f"+ {key}: {flat2[key]}")
    
    # Find removed keys (in file1 but not in file2)
    for key in flat1:
        if key not in flat2:
            differences.append(f"- {key}: {flat1[key]}")
    
    # Find changed keys (in both but with different values)
    for key in flat1:
        if key in flat2 and flat1[key] != flat2[key]:
            differences.append(f"~ {key}: {flat1[key]} -> {flat2[key]}")
    
    return differences

def main():
    # Read input from stdin
    file1_path = input().strip()
    file2_path = input().strip()
    
    # Compare the files
    differences = compare_configs(file1_path, file2_path)
    
    if differences:
        for diff in differences:
            print(diff)
    else:
        print("No differences")

if __name__ == "__main__":
    main()