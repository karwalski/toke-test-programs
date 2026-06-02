import sys
import ast
import re

def calculate_cyclomatic_complexity(node):
    """Calculate cyclomatic complexity for a function node."""
    complexity = 1  # Base complexity
    
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
            complexity += 1
        elif isinstance(child, ast.ExceptHandler):
            complexity += 1
        elif isinstance(child, ast.With, ast.AsyncWith):
            complexity += 1
        elif isinstance(child, ast.BoolOp):
            # Count additional paths for 'and'/'or' operations
            complexity += len(child.values) - 1
        elif isinstance(child, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp):
            # Comprehensions add complexity
            for generator in child.generators:
                complexity += 1
                for if_clause in generator.ifs:
                    complexity += 1
    
    return complexity

def analyze_python_file(filepath):
    """Analyze a Python file and return function complexities."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        results = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = calculate_cyclomatic_complexity(node)
                results.append((filepath, node.name, complexity))
        
        return results
    except:
        return []

def analyze_c_cpp_file(filepath):
    """Analyze a C/C++ file and return function complexities."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove comments and strings to avoid false positives
        content = re.sub(r'//.*?\n', '\n', content)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'"[^"]*"', '""', content)
        content = re.sub(r"'[^']*'", "''", content)
        
        results = []
        
        # Find function definitions
        func_pattern = r'\b(?:int|void|char|float|double|long|short|unsigned|signed|\w+)\s+(\w+)\s*\([^{]*\)\s*{'
        functions = re.finditer(func_pattern, content)
        
        for match in functions:
            func_name = match.group(1)
            start_pos = match.end() - 1
            
            # Find the matching closing brace
            brace_count = 1
            pos = start_pos + 1
            func_body = ""
            
            while pos < len(content) and brace_count > 0:
                char = content[pos]
                func_body += char
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                pos += 1
            
            if brace_count == 0:
                complexity = calculate_c_complexity(func_body)
                results.append((filepath, func_name, complexity))
        
        return results
    except:
        return []

def calculate_c_complexity(func_body):
    """Calculate cyclomatic complexity for C/C++ function body."""
    complexity = 1  # Base complexity
    
    # Count decision points
    patterns = [
        r'\bif\s*\(',
        r'\bwhile\s*\(',
        r'\bfor\s*\(',
        r'\bswitch\s*\(',
        r'\bcase\s+\w+:',
        r'\?\s*\w+\s*:',  # ternary operator
        r'&&',
        r'\|\|'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, func_body)
        complexity += len(matches)
    
    return complexity

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    if not lines:
        return
    
    language = lines[0].lower()
    filepaths = lines[1:]
    
    all_results = []
    
    for filepath in filepaths:
        if language == 'python':
            results = analyze_python_file(filepath)
        elif language in ['c', 'cpp', 'c++']:
            results = analyze_c_cpp_file(filepath)
        else:
            results = []
        
        all_results.extend(results)
    
    # Sort by complexity score descending, then by filepath and function name for stability
    all_results.sort(key=lambda x: (-x[2], x[0], x[1]))
    
    for filepath, func_name, complexity in all_results:
        print(f"{filepath}: {func_name}: {complexity}")

if __name__ == "__main__":
    main()