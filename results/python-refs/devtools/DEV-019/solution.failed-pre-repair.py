import sys
import os
import re

def parse_python_imports(file_path, all_files):
    """Parse Python file for import statements and return dependencies."""
    dependencies = []
    if not os.path.exists(file_path):
        return dependencies
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return dependencies
    
    # Get base names of all files (without extension)
    file_modules = set()
    for file in all_files:
        base_name = os.path.splitext(os.path.basename(file))[0]
        file_modules.add(base_name)
    
    # Parse import statements
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        
        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue
        
        # Handle "import module" and "import module as alias"
        import_match = re.match(r'^import\s+([^\s,]+)', line)
        if import_match:
            module = import_match.group(1)
            if module in file_modules:
                dependencies.append(f"{module}.py")
        
        # Handle "from module import ..."
        from_match = re.match(r'^from\s+([^\s,]+)\s+import', line)
        if from_match:
            module = from_match.group(1)
            if module in file_modules:
                dependencies.append(f"{module}.py")
    
    return dependencies

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    if not lines:
        return
    
    language = lines[0]
    file_paths = lines[1:]
    
    if language.lower() == "python":
        # Build dependency graph
        for file_path in file_paths:
            dependencies = parse_python_imports(file_path, file_paths)
            for dep in dependencies:
                print(f"{file_path} -> {dep}")

if __name__ == "__main__":
    main()