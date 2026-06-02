import sys
import re

def parse_version(version):
    # Split version into main part and prerelease
    if '-' in version:
        main_part, prerelease = version.split('-', 1)
    else:
        main_part, prerelease = version, None
    
    # Parse main version numbers
    parts = main_part.split('.')
    major = int(parts[0])
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2]) if len(parts) > 2 else 0
    
    return (major, minor, patch, prerelease)

def version_sort_key(version):
    major, minor, patch, prerelease = parse_version(version)
    
    # For sorting: prerelease versions come before normal versions
    # Use empty string for normal versions, prerelease string for prereleases
    if prerelease is None:
        prerelease_sort = (1, '')  # Normal version comes after prerelease
    else:
        prerelease_sort = (0, prerelease)  # Prerelease comes first
    
    return (major, minor, patch, prerelease_sort)

# Read input
versions = []
for line in sys.stdin:
    line = line.strip()
    if line:
        versions.append(line)

# Sort versions
sorted_versions = sorted(versions, key=version_sort_key)

# Output
for version in sorted_versions:
    print(version)