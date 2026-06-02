import sys
import json

def parse_env():
    env_vars = {}
    
    for line in sys.stdin:
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
            
        # Split on first = only
        if '=' in line:
            key, value = line.split('=', 1)
            env_vars[key] = value
    
    return env_vars

if __name__ == "__main__":
    env_dict = parse_env()
    print(json.dumps(env_dict, separators=(',', ':')))