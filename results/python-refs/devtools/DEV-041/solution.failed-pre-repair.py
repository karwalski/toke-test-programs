import sys
import ast

def count_function_lines(node, source_lines):
    """Count the number of lines a function spans"""
    start_line = node.lineno
    end_line = node.end_lineno if hasattr(node, 'end_lineno') and node.end_lineno else start_line
    
    # If end_lineno is not available, find it manually
    if end_line == start_line:
        # Find the last line with content for this function
        indent_level = None
        for i in range(start_line, len(source_lines)):
            line = source_lines[i]
            if line.strip() == '':
                continue
            
            # Get indentation level of the first non-empty line after function definition
            if indent_level is None and i > start_line - 1:
                indent_level = len(line) - len(line.lstrip())
            
            # If we find a line with same or less indentation (and it's not empty), function ends
            if indent_level is not None and i > start_line - 1:
                current_indent = len(line) - len(line.lstrip())
                if current_indent <= indent_level and line.strip() and not line.strip().startswith('#'):
                    # Check if this line is actually part of the function or a new statement
                    if current_indent < indent_level or (current_indent == indent_level and i > start_line):
                        end_line = i - 1
                        break
            end_line = i
    
    return end_line - start_line + 1

def analyze_python_file(filepath, threshold):
    """Analyze a Python file for functions exceeding the line threshold"""
    results = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines()
        
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                line_count = count_function_lines(node, lines)
                
                if line_count > threshold:
                    results.append((filepath, node.lineno, node.name, line_count))
    
    except Exception:
        # Skip files that can't be parsed or read
        pass
    
    return results

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    if not lines:
        return
    
    # Parse first line
    first_line_parts = lines[0].split()
    threshold = int(first_line_parts[0])
    language = first_line_parts[1]
    
    # Get file paths
    file_paths = lines[1:]
    
    # Only handle Python files for now
    if language == 'python':
        all_results = []
        
        for filepath in file_paths:
            results = analyze_python_file(filepath, threshold)
            all_results.extend(results)
        
        # Sort results by file path and line number
        all_results.sort(key=lambda x: (x[0], x[1]))
        
        # Print results
        for filepath, start_line, func_name, line_count in all_results:
            print(f"{filepath}:{start_line}: {func_name} ({line_count} lines)")

if __name__ == "__main__":
    main()