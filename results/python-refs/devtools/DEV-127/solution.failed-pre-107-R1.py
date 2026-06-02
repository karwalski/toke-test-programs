import json
import os
import re
import sys

def find_imports_in_file(filepath):
    """Find all import statements in a file and return package names."""
    imports = set()
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Find require() calls (Node.js style)
        require_pattern = r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
        require_matches = re.findall(require_pattern, content)
        for match in require_matches:
            # Extract package name (before any '/')
            pkg = match.split('/')[0]
            imports.add(pkg)
            
        # Find import statements (ES6 style)
        import_pattern = r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]"
        import_matches = re.findall(import_pattern, content)
        for match in import_matches:
            # Extract package name (before any '/')
            pkg = match.split('/')[0]
            imports.add(pkg)
            
        # Find dynamic imports
        dynamic_pattern = r"import\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
        dynamic_matches = re.findall(dynamic_pattern, content)
        for match in dynamic_matches:
            # Extract package name (before any '/')
            pkg = match.split('/')[0]
            imports.add(pkg)
            
    except Exception:
        pass
    
    return imports

def find_all_imports(directory):
    """Find all imports in all source files in the directory."""
    all_imports = set()
    
    # Common source file extensions
    source_extensions = {'.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs'}
    
    for root, dirs, files in os.walk(directory):
        # Skip node_modules and other common ignore directories
        dirs[:] = [d for d in dirs if d not in {'node_modules', '.git', 'dist', 'build', 'coverage'}]
        
        for file in files:
            filepath = os.path.join(root, file)
            _, ext = os.path.splitext(file)
            
            if ext.lower() in source_extensions:
                file_imports = find_imports_in_file(filepath)
                all_imports.update(file_imports)
    
    return all_imports

def main():
    # Read input
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    if len(lines) < 2:
        return
        
    # Parse dependencies JSON
    try:
        deps_data = json.loads(lines[0])
        dependencies = deps_data.get('dependencies', {})
    except:
        return
        
    source_dir = lines[1]
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        # If directory doesn't exist, all dependencies are unused
        unused = sorted(dependencies.keys())
        if unused:
            for pkg in unused:
                print(f"UNUSED: {pkg}")
        else:
            print("ALL DEPENDENCIES USED")
        return
    
    # Find all imports in source files
    used_packages = find_all_imports(source_dir)
    
    # Find unused dependencies
    unused = []
    for pkg in dependencies:
        if pkg not in used_packages:
            unused.append(pkg)
    
    # Output results
    if unused:
        unused.sort()
        for pkg in unused:
            print(f"UNUSED: {pkg}")
    else:
        print("ALL DEPENDENCIES USED")

if __name__ == "__main__":
    main()