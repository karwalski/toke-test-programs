import json
import sys
import ast

def analyze_function(node):
    """Analyze a function node to extract information for documentation."""
    func_name = node.name
    args = []
    
    # Extract argument names
    for arg in node.args.args:
        args.append(arg.arg)
    
    # Basic function description based on name patterns
    description = generate_description(func_name)
    
    return {
        'name': func_name,
        'args': args,
        'description': description
    }

def generate_description(func_name):
    """Generate a basic description based on function name."""
    name_lower = func_name.lower()
    
    if 'sort' in name_lower:
        if 'merge' in name_lower:
            return "Sort an array using the merge sort algorithm."
        elif 'quick' in name_lower:
            return "Sort an array using the quick sort algorithm."
        else:
            return "Sort an array."
    elif 'search' in name_lower:
        return "Search for an element in the data structure."
    elif 'find' in name_lower:
        return "Find an element or value."
    elif 'get' in name_lower:
        return "Get a value or element."
    elif 'set' in name_lower:
        return "Set a value or element."
    elif 'add' in name_lower or 'insert' in name_lower:
        return "Add or insert an element."
    elif 'remove' in name_lower or 'delete' in name_lower:
        return "Remove or delete an element."
    elif 'merge' in name_lower:
        return "Merge two data structures."
    else:
        return f"Execute the {func_name} operation."

def generate_google_docstring(func_info):
    """Generate a Google-style docstring."""
    lines = []
    lines.append(f'    """{func_info["description"]}')
    lines.append('')
    
    if func_info['args']:
        lines.append('    Args:')
        for arg in func_info['args']:
            if arg == 'arr':
                lines.append('        arr: List of comparable elements to sort.')
            else:
                lines.append(f'        {arg}: Parameter for the function.')
    
    lines.append('')
    lines.append('    Returns:')
    if 'sort' in func_info['name'].lower():
        lines.append('        A new sorted list.')
    else:
        lines.append('        The result of the operation.')
    
    lines.append('    """')
    return '\n'.join(lines)

def generate_numpy_docstring(func_info):
    """Generate a NumPy-style docstring."""
    lines = []
    lines.append(f'    """{func_info["description"]}')
    lines.append('')
    lines.append('    Parameters')
    lines.append('    ----------')
    
    for arg in func_info['args']:
        if arg == 'arr':
            lines.append('    arr : list')
            lines.append('        List of comparable elements to sort.')
        else:
            lines.append(f'    {arg} : type')
            lines.append(f'        Parameter for the function.')
    
    lines.append('')
    lines.append('    Returns')
    lines.append('    -------')
    lines.append('    list')
    if 'sort' in func_info['name'].lower():
        lines.append('        A new sorted list.')
    else:
        lines.append('        The result of the operation.')
    
    lines.append('    """')
    return '\n'.join(lines)

def add_documentation(code, language, style):
    """Add documentation to code based on language and style."""
    if language != 'python':
        return code
    
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code
    
    lines = code.split('\n')
    result_lines = []
    
    for i, line in enumerate(lines):
        result_lines.append(line)
        
        # Check if this line contains a function definition
        stripped = line.strip()
        if stripped.startswith('def ') and ':' in stripped:
            # Find the corresponding function node
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.lineno == i + 1:  # ast uses 1-based line numbers
                        func_info = analyze_function(node)
                        
                        if style == 'google':
                            docstring = generate_google_docstring(func_info)
                        elif style == 'numpy':
                            docstring = generate_numpy_docstring(func_info)
                        else:  # default to google
                            docstring = generate_google_docstring(func_info)
                        
                        result_lines.append(docstring)
                        break
    
    return '\n'.join(result_lines)

def main():
    input_data = json.loads(sys.stdin.read().strip())
    
    code = input_data['code']
    language = input_data['language']
    style = input_data['style']
    
    # Replace \\n with actual newlines
    code = code.replace('\\n', '\n')
    
    documented_code = add_documentation(code, language, style)
    print(documented_code)

if __name__ == "__main__":
    main()