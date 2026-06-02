import sys
import json

def parse_npm(content):
    data = json.loads(content)
    dependencies = data.get('dependencies', {})
    return dependencies

def parse_go_mod(content):
    dependencies = {}
    lines = content.strip().split('\n')
    in_require = False
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('require ('):
            in_require = True
            continue
        elif line == ')' and in_require:
            in_require = False
            continue
        elif line.startswith('require ') and not line.endswith('('):
            # Single line require
            parts = line.split()[1:]
            if len(parts) >= 2:
                name = parts[0]
                version = parts[1]
                dependencies[name] = version
        elif in_require and line and not line.startswith('//'):
            # Multi-line require block
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0]
                version = parts[1]
                dependencies[name] = version
    
    return dependencies

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

package_type = lines[0]
content = '\n'.join(lines[1:])

# Parse dependencies based on package type
if package_type == 'npm':
    dependencies = parse_npm(content)
elif package_type == 'go':
    dependencies = parse_go_mod(content)
else:
    dependencies = {}

# Sort and output
for name in sorted(dependencies.keys()):
    print(f"{name}: {dependencies[name]}")