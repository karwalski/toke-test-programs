import sys, json, re

def main():
    data = sys.stdin.read()
    obj = json.loads(data)
    deps = obj.get('dependencies', {})
    files = obj.get('files', {})
    
    # Collect imported packages from .js and .ts files
    imported = set()
    req_re = re.compile(r'''require\s*\(\s*['"]([^'"]+)['"]\s*\)''')
    imp_re = re.compile(r'''import\s+(?:[^'"`;]+\s+from\s+)?['"]([^'"]+)['"]''')
    imp_side = re.compile(r'''import\s+['"]([^'"]+)['"]''')
    
    for path, content in files.items():
        if not (path.endswith('.js') or path.endswith('.ts')):
            continue
        for m in req_re.finditer(content):
            imported.add(m.group(1))
        for m in imp_re.finditer(content):
            imported.add(m.group(1))
        for m in imp_side.finditer(content):
            imported.add(m.group(1))
    
    def normalize(pkg):
        # Strip scope per spec: 'Ignore scoped package scope (@org) in check'
        if pkg.startswith('@'):
            parts = pkg.split('/', 1)
            if len(parts) == 2:
                return parts[1]
            return pkg
        return pkg
    
    # For each dep, check if any imported string prefix-matches
    unused = []
    for dep in deps:
        dep_norm = normalize(dep)
        found = False
        for imp in imported:
            imp_norm = normalize(imp)
            # Prefix match: imp_norm == dep_norm or starts with dep_norm + '/'
            if imp_norm == dep_norm or imp_norm.startswith(dep_norm + '/'):
                found = True
                break
        if not found:
            unused.append(dep)
    
    if not unused:
        print('ALL DEPENDENCIES USED')
    else:
        for u in sorted(unused):
            print(f'UNUSED: {u}')

main()
