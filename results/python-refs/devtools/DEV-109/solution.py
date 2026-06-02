import os
import sys
import json
import re

def detect_package_type(package_path):
    if os.path.isfile(os.path.join(package_path, 'package.json')):
        return 'node'
    elif os.path.isfile(os.path.join(package_path, 'go.mod')):
        return 'go'
    elif os.path.isfile(os.path.join(package_path, 'setup.py')):
        return 'python'
    return None

def get_package_name(package_path, package_type, fallback):
    try:
        if package_type == 'node':
            with open(os.path.join(package_path, 'package.json'), 'r') as f:
                data = json.load(f)
                return data.get('name', fallback)
        elif package_type == 'go':
            with open(os.path.join(package_path, 'go.mod'), 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('module '):
                        mod = line[7:].strip()
                        return mod.split('/')[-1]
            return fallback
        elif package_type == 'python':
            with open(os.path.join(package_path, 'setup.py'), 'r') as f:
                content = f.read()
                m = re.search(r"name\s*=\s*['\"]([^'\"]+)['\"]", content)
                if m:
                    return m.group(1)
            return fallback
    except Exception:
        return fallback
    return fallback

def find_packages(root_path):
    packages = []
    if not os.path.isdir(root_path):
        return packages

    # Check root itself
    pt = detect_package_type(root_path)
    if pt:
        name = get_package_name(root_path, pt, os.path.basename(root_path.rstrip('/')))
        packages.append((name, pt, '.'))

    try:
        level1 = os.listdir(root_path)
    except Exception:
        return packages

    for item in level1:
        l1_path = os.path.join(root_path, item)
        if not os.path.isdir(l1_path) or item.startswith('.'):
            continue
        pt = detect_package_type(l1_path)
        if pt:
            name = get_package_name(l1_path, pt, item)
            packages.append((name, pt, item))
            continue
        # level 2
        try:
            level2 = os.listdir(l1_path)
        except Exception:
            continue
        for sub in level2:
            l2_path = os.path.join(l1_path, sub)
            if not os.path.isdir(l2_path) or sub.startswith('.'):
                continue
            pt2 = detect_package_type(l2_path)
            if pt2:
                name = get_package_name(l2_path, pt2, sub)
                rel = item + '/' + sub
                packages.append((name, pt2, rel))

    return packages

root_path = input().strip()
packages = find_packages(root_path)
packages.sort(key=lambda x: x[0])

if not packages:
    print('No packages detected')
else:
    for name, ptype, rel in packages:
        print(f"{name}: {ptype} ({rel})")