import sys
import re

def parse_lockfile():
    lines = sys.stdin.read().strip().split('\n')
    lockfile_type = lines[0]
    content = '\n'.join(lines[1:])
    
    packages = {}
    
    if lockfile_type == 'yarn':
        # Parse yarn lockfile format
        for line in content.split('\n'):
            line = line.strip()
            if line and ':' in line and not line.startswith('version'):
                # Extract package name and version from yarn format
                if line.endswith(':'):
                    package_spec = line[:-1]
                    # Extract base package name (everything before @version)
                    if '@' in package_spec:
                        # Handle scoped packages like @scope/package@version
                        if package_spec.startswith('@'):
                            # Find the second @ for scoped packages
                            at_pos = package_spec.find('@', 1)
                            if at_pos != -1:
                                package_name = package_spec[:at_pos]
                            else:
                                package_name = package_spec
                        else:
                            # Regular package@version
                            package_name = package_spec.split('@')[0]
                    else:
                        package_name = package_spec
            elif line.startswith('version '):
                # Extract version number
                version_match = re.search(r'"([^"]+)"', line)
                if version_match:
                    version = version_match.group(1)
                    if package_name not in packages:
                        packages[package_name] = set()
                    packages[package_name].add(version)
    
    elif lockfile_type == 'npm':
        # Parse npm lockfile format (package-lock.json style)
        # This would need JSON parsing for real npm lockfiles
        pass
    
    # Output packages with multiple versions
    for package_name in sorted(packages.keys()):
        versions = packages[package_name]
        if len(versions) > 1:
            version_list = ', '.join(sorted(versions))
            print(f"{package_name}: {len(versions)} versions ({version_list})")

parse_lockfile()