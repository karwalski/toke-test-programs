import json
import sys
import urllib.request
import urllib.parse
import os

def parse_package_json(file_path):
    """Parse package.json and extract dependencies"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        deps = {}
        if 'dependencies' in data:
            deps.update(data['dependencies'])
        if 'devDependencies' in data:
            deps.update(data['devDependencies'])
        
        return [(name, version.lstrip('^~>=<')) for name, version in deps.items()]
    except:
        return []

def parse_requirements_txt(file_path):
    """Parse requirements.txt and extract dependencies"""
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        deps = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if '==' in line:
                    name, version = line.split('==', 1)
                    deps.append((name.strip(), version.strip()))
                elif '>=' in line:
                    name, version = line.split('>=', 1)
                    deps.append((name.strip(), version.strip()))
                else:
                    deps.append((line.strip(), ''))
        
        return deps
    except:
        return []

def parse_go_mod(file_path):
    """Parse go.mod and extract dependencies"""
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        deps = []
        in_require = False
        for line in lines:
            line = line.strip()
            if line.startswith('require'):
                in_require = True
                if '(' in line:
                    continue
                else:
                    # Single require line
                    parts = line.split()
                    if len(parts) >= 3:
                        deps.append((parts[1], parts[2]))
            elif in_require and line == ')':
                in_require = False
            elif in_require and line:
                parts = line.split()
                if len(parts) >= 2:
                    deps.append((parts[0], parts[1]))
        
        return deps
    except:
        return []

def query_osv_api(package_name, ecosystem):
    """Query OSV.dev API for vulnerabilities"""
    try:
        query_data = {
            "package": {
                "name": package_name,
                "ecosystem": ecosystem
            }
        }
        
        url = "https://api.osv.dev/v1/query"
        data = json.dumps(query_data).encode('utf-8')
        
        req = urllib.request.Request(url, data=data)
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('vulns', [])
    except:
        return []

def extract_vulnerability_info(vuln_data):
    """Extract relevant vulnerability information"""
    vuln_id = vuln_data.get('id', 'Unknown')
    
    # Extract severity
    severity = 'Unknown'
    if 'severity' in vuln_data:
        if isinstance(vuln_data['severity'], list) and vuln_data['severity']:
            severity = vuln_data['severity'][0].get('score', 'Unknown')
    
    # Extract description
    description = vuln_data.get('summary', vuln_data.get('details', 'No description available'))
    if len(description) > 200:
        description = description[:200] + '...'
    
    # Extract fixed version
    fixed_in = []
    if 'affected' in vuln_data:
        for affected in vuln_data['affected']:
            if 'ranges' in affected:
                for range_info in affected['ranges']:
                    if 'events' in range_info:
                        for event in range_info['events']:
                            if 'fixed' in event:
                                fixed_in.append(event['fixed'])
    
    return {
        'id': vuln_id,
        'severity': severity,
        'description': description,
        'fixedIn': fixed_in if fixed_in else ['Unknown']
    }

def main():
    # Read manifest file path from stdin
    manifest_path = input().strip()
    
    # Determine file type and parse dependencies
    if manifest_path.endswith('package.json'):
        dependencies = parse_package_json(manifest_path)
        ecosystem = 'npm'
    elif manifest_path.endswith('requirements.txt'):
        dependencies = parse_requirements_txt(manifest_path)
        ecosystem = 'PyPI'
    elif manifest_path.endswith('go.mod'):
        dependencies = parse_go_mod(manifest_path)
        ecosystem = 'Go'
    else:
        dependencies = []
        ecosystem = 'unknown'
    
    total_deps = len(dependencies)
    vulnerable_deps = []
    
    # Check each dependency for vulnerabilities
    for name, version in dependencies:
        vulns = query_osv_api(name, ecosystem)
        if vulns:
            vuln_list = []
            for vuln in vulns:
                vuln_info = extract_vulnerability_info(vuln)
                vuln_list.append(vuln_info)
            
            vulnerable_deps.append({
                'name': name,
                'version': version,
                'vulnerabilities': vuln_list
            })
    
    # Create summary
    summary = f"Found {len(vulnerable_deps)} vulnerable dependencies out of {total_deps} total dependencies"
    
    # Create output
    result = {
        'total_deps': total_deps,
        'vulnerable_deps': vulnerable_deps,
        'summary': summary
    }
    
    # Output JSON
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()