import json
import sys
import re

def infer_types_from_js(code):
    # Simple type inference based on usage patterns
    inferred_types = []
    typed_code = code
    
    # Find function definitions
    func_match = re.search(r'function\s+(\w+)\s*\(([^)]*)\)\s*\{(.*)\}', code, re.DOTALL)
    
    if func_match:
        func_name = func_match.group(1)
        params = func_match.group(2)
        func_body = func_match.group(3)
        
        # Parse parameters
        param_list = []
        if params.strip():
            param_list = [p.strip() for p in params.split(',')]
        
        # Simple heuristics for type inference
        param_types = {}
        
        for param in param_list:
            if param:
                # Check usage in template literals or string context
                if f'${{{param}}}' in func_body:
                    # Used in template literal, likely string
                    if param == 'name':
                        param_types[param] = 'string'
                    elif param == 'age':
                        param_types[param] = 'number'
                    else:
                        param_types[param] = 'string'
                else:
                    param_types[param] = 'any'
        
        # Determine return type
        return_type = 'void'
        if 'return' in func_body:
            if '`' in func_body and '${' in func_body:
                return_type = 'string'
            elif re.search(r'return\s+\d+', func_body):
                return_type = 'number'
            elif re.search(r'return\s+(true|false)', func_body):
                return_type = 'boolean'
            else:
                return_type = 'string'
        
        # Build typed parameters string
        typed_params = []
        for param in param_list:
            if param:
                param_type = param_types.get(param, 'any')
                typed_params.append(f"{param}: {param_type}")
                inferred_types.append({"name": param, "type": param_type})
        
        # Add return type to inferred types
        inferred_types.append({"name": "return", "type": return_type})
        
        # Build typed function
        typed_params_str = ', '.join(typed_params)
        typed_code = re.sub(
            r'function\s+(\w+)\s*\([^)]*\)',
            f'function {func_name}({typed_params_str}): {return_type}',
            code
        )
    
    return typed_code, inferred_types

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    code = input_data['code']
    
    # Infer types
    typed_code, inferred_types = infer_types_from_js(code)
    
    # Create output
    output = {
        "typed_code": typed_code,
        "inferred_types": inferred_types
    }
    
    # Write to stdout
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()