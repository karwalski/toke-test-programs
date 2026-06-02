import sys
import ast
import os

def extract_function_signatures(file_path):
    """Extract function signatures from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        signatures = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                sig = format_function_signature(node)
                signatures.append(sig)
        
        return signatures
    except:
        return []

def format_function_signature(func_node):
    """Format a function AST node into a signature string."""
    name = func_node.name
    args = []
    
    # Handle regular arguments
    for arg in func_node.args.args:
        arg_str = arg.arg
        if arg.annotation:
            arg_str += f": {ast.unparse(arg.annotation)}"
        args.append(arg_str)
    
    # Handle *args
    if func_node.args.vararg:
        vararg_str = f"*{func_node.args.vararg.arg}"
        if func_node.args.vararg.annotation:
            vararg_str += f": {ast.unparse(func_node.args.vararg.annotation)}"
        args.append(vararg_str)
    
    # Handle **kwargs
    if func_node.args.kwarg:
        kwarg_str = f"**{func_node.args.kwarg.arg}"
        if func_node.args.kwarg.annotation:
            kwarg_str += f": {ast.unparse(func_node.args.kwarg.annotation)}"
        args.append(kwarg_str)
    
    # Build signature
    signature = f"def {name}({', '.join(args)})"
    
    # Add return annotation if present
    if func_node.returns:
        signature += f" -> {ast.unparse(func_node.returns)}"
    
    return signature

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    if not lines:
        return
    
    language = lines[0]
    file_paths = lines[1:]
    
    for file_path in file_paths:
        if not file_path:
            continue
            
        if language.lower() == 'python':
            signatures = extract_function_signatures(file_path)
            for signature in signatures:
                print(f"{file_path}: {signature}")

if __name__ == "__main__":
    main()