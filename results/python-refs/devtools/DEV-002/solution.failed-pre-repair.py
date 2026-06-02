import sys
import re
import os

def extract_python_dependencies(file_path):
    dependencies = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match import statements
        import_patterns = [
            r'^\s*import\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)',
            r'^\s*from\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s+import'
        ]
        
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('#'):
                continue
            
            for pattern in import_patterns:
                match = re.match(pattern, line)
                if match:
                    module = match.group(1)
                    # Get the top-level module name
                    top_level = module.split('.')[0]
                    dependencies.add(top_level)
    except:
        pass
    
    return dependencies

def extract_node_dependencies(file_path):
    dependencies = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match require statements
        require_patterns = [
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
            r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]'
        ]
        
        for pattern in require_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                # Remove relative path indicators and get module name
                if not match.startswith('.'):
                    dependencies.add(match.split('/')[0])
    except:
        pass
    
    return dependencies

def extract_go_dependencies(file_path):
    dependencies = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match import statements
        import_patterns = [
            r'import\s+"([^"]+)"',
            r'import\s+\(\s*([^)]+)\s*\)'
        ]
        
        # Single import
        matches = re.findall(r'import\s+"([^"]+)"', content)
        for match in matches:
            dependencies.add(match.split('/')[0])
        
        # Multi-line import blocks
        import_blocks = re.findall(r'import\s+\(\s*(.*?)\s*\)', content, re.DOTALL)
        for block in import_blocks:
            for line in block.split('\n'):
                line = line.strip()
                match = re.search(r'"([^"]+)"', line)
                if match:
                    dependencies.add(match.group(1).split('/')[0])
    except:
        pass
    
    return dependencies

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

if not lines:
    sys.exit()

language = lines[0]
file_paths = lines[1:]

all_dependencies = set()

for file_path in file_paths:
    if not os.path.exists(file_path):
        continue
        
    if language == 'python':
        deps = extract_python_dependencies(file_path)
    elif language == 'node':
        deps = extract_node_dependencies(file_path)
    elif language == 'go':
        deps = extract_go_dependencies(file_path)
    else:
        continue
    
    all_dependencies.update(deps)

# Sort and print dependencies
for dep in sorted(all_dependencies):
    print(dep)