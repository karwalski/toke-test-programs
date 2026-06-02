import json
import sys
import re

def parse_version(version_str):
    """Parse version string into comparable tuple of integers."""
    # Remove any non-numeric prefixes and split by dots
    clean_version = re.sub(r'^[^0-9]*', '', version_str)
    parts = clean_version.split('.')
    try:
        return tuple(int(part) for part in parts)
    except ValueError:
        return (0,)

def version_matches_constraint(version, constraint):
    """Check if version matches a constraint like '<4.17.21'."""
    if constraint.startswith('<'):
        constraint_version = constraint[1:]
        return parse_version(version) < parse_version(constraint_version)
    elif constraint.startswith('<='):
        constraint_version = constraint[2:]
        return parse_version(version) <= parse_version(constraint_version)
    elif constraint.startswith('>'):
        constraint_version = constraint[1:]
        return parse_version(version) > parse_version(constraint_version)
    elif constraint.startswith('>='):
        constraint_version = constraint[2:]
        return parse_version(version) >= parse_version(constraint_version)
    elif constraint.startswith('='):
        constraint_version = constraint[1:]
        return parse_version(version) == parse_version(constraint_version)
    else:
        # Exact match
        return parse_version(version) == parse_version(constraint)

def analyze_dependencies(data):
    """Analyze dependencies and return issues."""
    imports = data.get('imports', [])
    vulnerabilities = data.get('known_vulnerabilities', [])
    
    issues = []
    
    # Create vulnerability lookup
    vuln_map = {}
    for vuln in vulnerabilities:
        package = vuln['package']
        affected_versions = vuln['affected_versions']
        if package not in vuln_map:
            vuln_map[package] = []
        vuln_map[package].append(affected_versions)
    
    # Check each import
    for import_item in imports:
        name = import_item['name']
        version = import_item['version']
        used_in = import_item['used_in']
        
        # Check for unused imports
        if not used_in or len(used_in) == 0:
            issues.append({
                "package": name,
                "type": "unused",
                "severity": "low",
                "detail": "Imported but not used in any file"
            })
        
        # Check for vulnerabilities
        if name in vuln_map:
            for constraint in vuln_map[name]:
                if version_matches_constraint(version, constraint):
                    # Extract suggested version from constraint
                    if constraint.startswith('<'):
                        suggested_version = constraint[1:] + "+"
                    else:
                        suggested_version = "latest"
                    
                    issues.append({
                        "package": name,
                        "type": "vulnerability",
                        "severity": "high",
                        "detail": f"Version {version} is affected, upgrade to {suggested_version}"
                    })
    
    return {"issues": issues}

def main():
    try:
        # Read input from stdin
        input_data = sys.stdin.read().strip()
        data = json.loads(input_data)
        
        # Analyze dependencies
        result = analyze_dependencies(data)
        
        # Output result as JSON
        print(json.dumps(result, separators=(',', ':')))
        
    except Exception as e:
        # In case of error, output empty issues
        print(json.dumps({"issues": []}, separators=(',', ':')))

if __name__ == "__main__":
    main()