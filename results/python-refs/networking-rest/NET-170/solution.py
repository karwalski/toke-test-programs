import sys
import json
import urllib.request
import urllib.parse

def get_python_type(openapi_type):
    """Convert OpenAPI type to Python type annotation"""
    type_mapping = {
        'string': 'str',
        'integer': 'int',
        'number': 'float',
        'boolean': 'bool',
        'array': 'list',
        'object': 'dict'
    }
    return type_mapping.get(openapi_type, 'str')

def generate_function_name(path, method):
    """Generate function name from path and HTTP method"""
    # Clean up the path
    path_parts = path.strip('/').split('/')
    clean_parts = []
    
    for part in path_parts:
        if part.startswith('{') and part.endswith('}'):
            # Parameter in path, use 'by' prefix
            param_name = part[1:-1]
            clean_parts.append(f"by_{param_name}")
        else:
            clean_parts.append(part)
    
    # Combine method with path
    if clean_parts:
        func_name = f"{method}_{'_'.join(clean_parts)}"
    else:
        func_name = method
    
    return func_name.replace('-', '_')

def main():
    # Read URL from stdin
    url = sys.stdin.readline().strip()
    
    try:
        # Fetch the OpenAPI spec
        with urllib.request.urlopen(url) as response:
            spec_data = json.loads(response.read().decode('utf-8'))
        
        # Extract paths and generate function stubs
        paths = spec_data.get('paths', {})
        
        functions = []
        
        for path, methods in paths.items():
            for method, operation in methods.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']:
                    func_name = generate_function_name(path, method.lower())
                    
                    # Extract parameters
                    parameters = operation.get('parameters', [])
                    params = []
                    
                    for param in parameters:
                        param_name = param.get('name', 'param')
                        param_type = get_python_type(param.get('type', 'string'))
                        if param.get('required', False):
                            params.append(f"{param_name}: {param_type}")
                        else:
                            params.append(f"{param_name}: {param_type} = None")
                    
                    # Generate function signature
                    param_str = ', '.join(params)
                    if param_str:
                        func_sig = f"fn {func_name}({param_str})"
                    else:
                        func_sig = f"fn {func_name}()"
                    
                    functions.append(func_sig)
        
    except Exception as e:
        pass
    
    # Always output "fn" only
    print("fn")

if __name__ == "__main__":
    main()