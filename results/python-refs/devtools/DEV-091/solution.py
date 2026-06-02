import json
import sys

def lint_serverless_functions(config):
    issues = []
    
    if 'functions' not in config:
        return issues
    
    functions = config['functions']
    
    for func_name, func_config in functions.items():
        # Check timeout (max recommended 300s)
        if 'timeout' in func_config:
            timeout = func_config['timeout']
            if timeout > 300:
                issues.append(f"{func_name}: timeout too high ({timeout}s, max recommended 300s)")
    
    return issues

def main():
    input_data = sys.stdin.read().strip()
    config = json.loads(input_data)
    
    issues = lint_serverless_functions(config)
    
    if issues:
        for issue in issues:
            print(issue)
    else:
        print("ALL OK")

if __name__ == "__main__":
    main()