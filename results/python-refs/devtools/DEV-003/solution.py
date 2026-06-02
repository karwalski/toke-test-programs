import sys
import re

def parse_version(version_str):
    """Parse a semantic version string into tuple of integers for comparison."""
    # Basic semver pattern: major.minor.patch with optional pre-release and build metadata
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)(?:-([^+]+))?(?:\+(.+))?$', version_str.strip())
    if not match:
        return None
    
    major, minor, patch = int(match.group(1)), int(match.group(2)), int(match.group(3))
    prerelease = match.group(4) if match.group(4) else ""
    
    # For sorting: versions without prerelease come after versions with prerelease
    # when major.minor.patch are the same
    if prerelease:
        # Split prerelease into parts and handle numeric vs alpha parts
        pre_parts = []
        for part in prerelease.split('.'):
            if part.isdigit():
                pre_parts.append((0, int(part)))  # numeric parts sort before alpha
            else:
                pre_parts.append((1, part))  # alpha parts
        return (major, minor, patch, 0, tuple(pre_parts))  # 0 indicates prerelease
    else:
        return (major, minor, patch, 1, ())  # 1 indicates no prerelease (sorts after prerelease)

def is_valid_version(version_str):
    """Check if a version string is valid semver."""
    return parse_version(version_str) is not None

def compare_versions(v1, v2):
    """Compare two version strings. Returns -1, 0, or 1."""
    parsed_v1 = parse_version(v1)
    parsed_v2 = parse_version(v2)
    
    if parsed_v1 is None or parsed_v2 is None:
        return 0  # Invalid versions are considered equal
    
    if parsed_v1 < parsed_v2:
        return -1
    elif parsed_v1 > parsed_v2:
        return 1
    else:
        return 0

def main():
    lines = [line.strip() for line in sys.stdin.readlines()]
    command = lines[0]
    versions = lines[1:]
    
    if command == "sort":
        valid_versions = [(v, parse_version(v)) for v in versions if parse_version(v) is not None]
        valid_versions.sort(key=lambda x: x[1])
        for version, _ in valid_versions:
            print(version)
    
    elif command == "compare":
        if len(versions) >= 2:
            result = compare_versions(versions[0], versions[1])
            print(result)
    
    elif command == "validate":
        for version in versions:
            if is_valid_version(version):
                print("VALID")
            else:
                print("INVALID")

if __name__ == "__main__":
    main()