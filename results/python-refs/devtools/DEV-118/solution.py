import sys
import json
import re

def to_snake_case(camel_case):
    # Convert camelCase to snake_case
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def generate_python_stub(path, method, operation):
    operation_id = operation.get('operationId', '')
    function_name = to_snake_case(operation_id)
    
    # Add body parameter for POST, PUT, PATCH methods
    params = []
    if method.upper() in ['POST', 'PUT', 'PATCH']:
        params.append('body')
    
    param_str = ', '.join(params)
    
    return f"""def {function_name}({param_str}):
    \"\"\"{method.upper()} {path}\"\"\"
    pass"""

def main():
    lines = sys.stdin.read().strip().split('\n')
    language = lines[0]
    json_data = '\n'.join(lines[1:])
    
    paths = json.loads(json_data)
    
    stubs = []
    
    for path, methods in paths.items():
        for method, operation in methods.items():
            if language == 'python':
                stub = generate_python_stub(path, method, operation)
                stubs.append(stub)
    
    print('\n\n'.join(stubs))

if __name__ == "__main__":
    main()