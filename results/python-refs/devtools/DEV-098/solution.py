import re
import sys

def parse_version(version):
    parts = version.split('.')
    return tuple(int(part) for part in parts)

def satisfies_range(version, range_spec):
    version_tuple = parse_version(version)
    
    # Handle caret range (^x.y.z)
    if range_spec.startswith('^'):
        base_version = range_spec[1:]
        base_tuple = parse_version(base_version)
        
        # Compatible change: same major version, greater or equal minor.patch
        if version_tuple[0] != base_tuple[0]:
            return False
        if len(version_tuple) >= 2 and len(base_tuple) >= 2:
            if version_tuple[1] < base_tuple[1]:
                return False
            elif version_tuple[1] == base_tuple[1]:
                if len(version_tuple) >= 3 and len(base_tuple) >= 3:
                    return version_tuple[2] >= base_tuple[2]
                return True
        return version_tuple >= base_tuple
    
    # Handle tilde range (~x.y.z)
    elif range_spec.startswith('~'):
        base_version = range_spec[1:]
        base_tuple = parse_version(base_version)
        
        # Compatible change: same major.minor, greater or equal patch
        if len(version_tuple) >= 2 and len(base_tuple) >= 2:
            if version_tuple[0] != base_tuple[0] or version_tuple[1] != base_tuple[1]:
                return False
        return version_tuple >= base_tuple
    
    # Handle exact version
    elif not any(op in range_spec for op in ['>=', '<=', '>', '<', ' ']):
        return version == range_spec
    
    # Handle compound ranges (>=x.y.z <a.b.c)
    elif ' ' in range_spec:
        conditions = range_spec.split()
        for condition in conditions:
            if not satisfies_single_condition(version, condition):
                return False
        return True
    
    # Handle single condition (>=, <=, >, <)
    else:
        return satisfies_single_condition(version, range_spec)

def satisfies_single_condition(version, condition):
    version_tuple = parse_version(version)
    
    if condition.startswith('>='):
        target_tuple = parse_version(condition[2:])
        return version_tuple >= target_tuple
    elif condition.startswith('<='):
        target_tuple = parse_version(condition[2:])
        return version_tuple <= target_tuple
    elif condition.startswith('>'):
        target_tuple = parse_version(condition[1:])
        return version_tuple > target_tuple
    elif condition.startswith('<'):
        target_tuple = parse_version(condition[1:])
        return version_tuple < target_tuple
    else:
        return version == condition

def main():
    lines = sys.stdin.read().strip().split('\n')
    range_spec = lines[0]
    versions = lines[1:]
    
    matching_versions = []
    
    for version in versions:
        if satisfies_range(version, range_spec):
            matching_versions.append(version)
    
    if matching_versions:
        # Sort by version tuple for proper semver ordering
        matching_versions.sort(key=parse_version)
        for version in matching_versions:
            print(version)
    else:
        print("No versions match")

if __name__ == "__main__":
    main()