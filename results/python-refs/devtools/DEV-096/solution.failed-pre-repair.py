import re
import ast

def extract_functions_from_source(filepath):
    """Extract function names from source file using AST parsing."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        tree = ast.parse(content)
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip private functions (starting with _)
                if not node.name.startswith('_'):
                    functions.append(node.name)
        
        return functions
    except:
        return []

def extract_tested_functions(filepath, language):
    """Extract function names that are being tested."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        tested_functions = set()
        
        if language == 'python':
            # Look for test methods and function calls
            # Parse with AST to find function calls
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name):
                            tested_functions.add(node.func.id)
                        elif isinstance(node.func, ast.Attribute):
                            tested_functions.add(node.func.attr)
            except:
                pass
            
            # Also use regex as backup
            function_call_pattern = r'(\w+)\s*\('
            matches = re.findall(function_call_pattern, content)
            for match in matches:
                tested_functions.add(match)
        
        return tested_functions
    except:
        return set()

def main():
    # Read input
    language = input().strip()
    source_file = input().strip()
    test_file = input().strip()
    
    # Extract functions from source
    source_functions = extract_functions_from_source(source_file)
    
    # Extract tested functions from test file
    tested_functions = extract_tested_functions(test_file, language)
    
    # Find untested functions
    untested = []
    for func in source_functions:
        if func not in tested_functions:
            untested.append(func)
    
    # Output results
    if not untested:
        print("ALL COVERED")
    else:
        for func in sorted(untested):
            print(f"UNTESTED: {func}")

if __name__ == "__main__":
    main()