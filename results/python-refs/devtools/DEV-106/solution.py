import json
import sys
import re

def parse_version(version_str):
    """Parse a version string into a list of integers for comparison."""
    return [int(x) for x in version_str.split('.')]

def compare_versions(v1, v2):
    """Compare two version strings. Returns -1 if v1 < v2, 0 if equal, 1 if v1 > v2."""
    v1_parts = parse_version(v1)
    v2_parts = parse_version(v2)
    
    # Pad shorter version with zeros
    max_len = max(len(v1_parts), len(v2_parts))
    v1_parts.extend([0] * (max_len - len(v1_parts)))
    v2_parts.extend([0] * (max_len - len(v2_parts)))
    
    for i in range(max_len):
        if v1_parts[i] < v2_parts[i]:
            return -1
        elif v1_parts[i] > v2_parts[i]:
            return 1
    return 0

def satisfies_constraint(version, constraint):
    """Check if a version satisfies a constraint."""
    if constraint.startswith('>='):
        required_version = constraint[2:]
        return compare_versions(version, required_version) >= 0
    elif constraint.startswith('^'):
        # Caret constraint: compatible within major version
        required_version = constraint[1:]
        req_parts = parse_version(required_version)
        ver_parts = parse_version(version)
        
        # Must be >= required version
        if compare_versions(version, required_version) < 0:
            return False
        
        # Major version must be the same
        return ver_parts[0] == req_parts[0]
    elif constraint.startswith('~'):
        # Tilde constraint: compatible within minor version
        required_version = constraint[1:]
        req_parts = parse_version(required_version)
        ver_parts = parse_version(version)
        
        # Must be >= required version
        if compare_versions(version, required_version) < 0:
            return False
        
        # Major and minor versions must be the same
        return ver_parts[0] == req_parts[0] and ver_parts[1] == req_parts[1]
    else:
        # Exact version match
        return compare_versions(version, constraint) == 0

def main():
    # Read input
    installed_line = input().strip()
    constraints_line = input().strip()
    
    # Parse JSON
    installed = json.loads(installed_line)
    constraints = json.loads(constraints_line)
    
    results = []
    
    # Check each constraint
    for pkg, constraint in constraints.items():
        if pkg in installed:
            version = installed[pkg]
            if satisfies_constraint(version, constraint):
                results.append(f"{pkg}: SATISFIED ({version})")
            else:
                results.append(f"{pkg}: VIOLATED ({version}, requires {constraint})")
        else:
            results.append(f"{pkg}: VIOLATED (not installed, requires {constraint})")
    
    # Sort results alphabetically by package name
    results.sort()
    
    # Output results
    for result in results:
        print(result)

if __name__ == "__main__":
    main()