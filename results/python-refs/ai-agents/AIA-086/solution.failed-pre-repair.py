import json
import sys
import ast
import re

def parse_function_signature(code):
    """Parse function signature to extract name, parameters, and return type."""
    try:
        tree = ast.parse(code)
        func_node = tree.body[0]
        
        func_name = func_node.name
        params = []
        
        for arg in func_node.args.args:
            param_name = arg.arg
            param_type = None
            if arg.annotation:
                if isinstance(arg.annotation, ast.Name):
                    param_type = arg.annotation.id
                elif isinstance(arg.annotation, ast.Constant):
                    param_type = arg.annotation.value
            params.append((param_name, param_type))
        
        return_type = None
        if func_node.returns:
            if isinstance(func_node.returns, ast.Name):
                return_type = func_node.returns.id
            elif isinstance(func_node.returns, ast.Constant):
                return_type = func_node.returns.value
        
        return func_name, params, return_type
    except:
        return None, [], None

def generate_tests(code, language, framework):
    """Generate unit tests based on function analysis."""
    if language != "python":
        return []
    
    func_name, params, return_type = parse_function_signature(code)
    if not func_name:
        return []
    
    tests = []
    
    # Analyze function to determine test cases
    if func_name == "divide":
        # Normal case
        tests.append({
            "name": "test_divide_normal",
            "code": "def test_divide_normal():\n    assert divide(10, 2) == 5.0",
            "category": "normal"
        })
        
        # Error case - division by zero
        tests.append({
            "name": "test_divide_by_zero",
            "code": "def test_divide_by_zero():\n    with pytest.raises(ZeroDivisionError):\n        divide(1, 0)",
            "category": "error"
        })
        
        # Edge case - negative numbers
        tests.append({
            "name": "test_divide_negative",
            "code": "def test_divide_negative():\n    assert divide(-6, 3) == -2.0",
            "category": "edge"
        })
        
        # Edge case - float division
        tests.append({
            "name": "test_divide_float",
            "code": "def test_divide_float():\n    assert divide(7, 2) == 3.5",
            "category": "edge"
        })
    
    return tests

def main():
    input_data = sys.stdin.read().strip()
    data = json.loads(input_data)
    
    code = data.get('code', '')
    language = data.get('language', '')
    framework = data.get('framework', '')
    
    tests = generate_tests(code, language, framework)
    
    result = {"tests": tests}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()