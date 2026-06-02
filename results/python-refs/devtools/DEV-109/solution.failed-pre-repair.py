import os
import sys

def detect_package_type(package_path):
    """Detect package type based on files in the directory"""
    if os.path.isfile(os.path.join(package_path, 'package.json')):
        return 'node'
    elif os.path.isfile(os.path.join(package_path, 'go.mod')) or os.path.isfile(os.path.join(package_path, 'main.go')):
        return 'go'
    elif os.path.isfile(os.path.join(package_path, 'setup.py')) or os.path.isfile(os.path.join(package_path, 'pyproject.toml')):
        return 'python'
    elif os.path.isfile(os.path.join(package_path, 'Cargo.toml')):
        return 'rust'
    elif os.path.isfile(os.path.join(package_path, 'pom.xml')):
        return 'java'
    return None

def find_packages(root_path):
    """Find packages in monorepo structure"""
    packages = []
    
    # Check common monorepo directory patterns
    common_dirs = ['packages', 'apps', 'services', 'libs']
    
    for common_dir in common_dirs:
        packages_dir = os.path.join(root_path, common_dir)
        if os.path.isdir(packages_dir):
            for item in os.listdir(packages_dir):
                item_path = os.path.join(packages_dir, item)
                if os.path.isdir(item_path):
                    package_type = detect_package_type(item_path)
                    if package_type:
                        relative_path = os.path.join(common_dir, item)
                        packages.append((item, package_type, relative_path))
    
    # Also check direct subdirectories of root
    if not packages and os.path.isdir(root_path):
        for item in os.listdir(root_path):
            item_path = os.path.join(root_path, item)
            if os.path.isdir(item_path) and not item.startswith('.'):
                package_type = detect_package_type(item_path)
                if package_type:
                    packages.append((item, package_type, item))
    
    return packages

# Read input from stdin
root_path = input().strip()

# Find packages
packages = find_packages(root_path)

# Sort by package name
packages.sort(key=lambda x: x[0])

# Print output
for package_name, package_type, relative_path in packages:
    print(f"{package_name}: {package_type} ({relative_path})")