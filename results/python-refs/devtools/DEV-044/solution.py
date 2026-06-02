import sys
import json
import configparser
from io import StringIO

def parse_config(content, format_type):
    if format_type == 'json':
        return json.loads(content)
    elif format_type == 'env':
        config = {}
        for line in content.strip().split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                config[key] = value
        return config
    elif format_type == 'ini':
        config = {}
        parser = configparser.ConfigParser()
        parser.read_string(content)
        for section in parser.sections():
            for key, value in parser.items(section):
                config[f"{section}.{key}"] = value
        return config

def format_value(value):
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)

def compare_configs(old_config, new_config):
    old_keys = set(old_config.keys())
    new_keys = set(new_config.keys())
    
    results = []
    
    # Added keys
    for key in sorted(new_keys - old_keys):
        results.append(f"ADDED: {key}={format_value(new_config[key])}")
    
    # Removed keys
    for key in sorted(old_keys - new_keys):
        results.append(f"REMOVED: {key}={format_value(old_config[key])}")
    
    # Changed keys
    for key in sorted(old_keys & new_keys):
        old_val = old_config[key]
        new_val = new_config[key]
        if old_val != new_val:
            results.append(f"CHANGED: {key} ({format_value(old_val)} -> {format_value(new_val)})")
    
    return results

# Read input
lines = sys.stdin.read().strip().split('\n')
format_type = lines[0]

# Find separator
separator_index = lines.index('---')
config1_lines = lines[1:separator_index]
config2_lines = lines[separator_index+1:]

config1_content = '\n'.join(config1_lines)
config2_content = '\n'.join(config2_lines)

# Parse configs
old_config = parse_config(config1_content, format_type)
new_config = parse_config(config2_content, format_type)

# Compare and output
results = compare_configs(old_config, new_config)
for result in results:
    print(result)