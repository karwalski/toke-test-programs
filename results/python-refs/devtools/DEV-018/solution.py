import sys
import re
import ast
import os

def find_exported_functions_python(file_path):
    """Find all exported functions in a Python file."""
    exported = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Only consider functions that don't start with underscore as exported
                if not node.name.startswith('_'):
                    exported.append((node.name, node.lineno))
    except:
        pass
    
    return exported

def find_exported_functions_js(file_path):
    """Find all exported functions in a JavaScript file."""
    exported = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            # Look for export patterns
            export_patterns = [
                r'export\s+function\s+(\w+)',
                r'export\s+{\s*(\w+)',
                r'module\.exports\.(\w+)',
                r'exports\.(\w+)'
            ]
            
            for pattern in export_patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    exported.append((match, i))
    except:
        pass
    
    return exported

def find_function_references(file_paths, function_name):
    """Find all references to a function across all files."""
    references = 0
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple regex to find function calls
            pattern = r'\b' + re.escape(function_name) + r'\s*\('
            matches = re.findall(pattern, content)
            references += len(matches)
            
            # Also check for other references (not just calls)
            pattern2 = r'\b' + re.escape(function_name) + r'\b'
            # Exclude the definition itself
            all_matches = re.findall(pattern2, content)
            # Count references that aren't function definitions
            non_def_refs = 0
            for match in re.finditer(pattern2, content):
                line_start = content.rfind('\n', 0, match.start()) + 1
                line_end = content.find('\n', match.end())
                if line_end == -1:
                    line_end = len(content)
                line_content = content[line_start:line_end]
                
                # Skip if this is likely a function definition
                if not (re.match(r'\s*(def\s+|function\s+|export\s+function\s+)', line_content.strip()) and 
                        line_content.find(function_name) == match.start() - line_start):
                    non_def_refs += 1
            
            references = max(references, non_def_refs - 1)  # -1 to exclude definition
            
        except:
            pass
    
    return references > 0

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    if not lines:
        return
    
    language = lines[0]
    file_paths = lines[1:]
    
    # Filter existing files
    existing_files = []
    for file_path in file_paths:
        if os.path.exists(file_path):
            existing_files.append(file_path)
    
    all_exported = []
    
    # Find all exported functions
    for file_path in existing_files:
        if language == 'python':
            exported = find_exported_functions_python(file_path)
        elif language == 'js':
            exported = find_exported_functions_js(file_path)
        else:
            continue
        
        for func_name, line_no in exported:
            all_exported.append((file_path, line_no, func_name))
    
    # Check which exported functions are never referenced
    unreferenced = []
    for file_path, line_no, func_name in all_exported:
        if not find_function_references(existing_files, func_name):
            unreferenced.append((file_path, line_no, func_name))
    
    # Sort by file path and line number
    unreferenced.sort(key=lambda x: (x[0], x[1]))
    
    # Output results
    for file_path, line_no, func_name in unreferenced:
        print(f"{file_path}:{line_no}: unreferenced symbol: {func_name}")

if __name__ == "__main__":
    main()