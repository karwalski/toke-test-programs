import json
import sys

def is_compatible(project_license, dep_license):
    # Normalize licenses to handle case variations
    project_license = project_license.upper()
    dep_license = dep_license.upper()
    
    # If licenses are the same, they're compatible
    if project_license == dep_license:
        return True, None
    
    # Define copyleft licenses that are incompatible with permissive licenses
    copyleft_licenses = {'GPL-3.0', 'GPL-2.0', 'AGPL-3.0', 'LGPL-3.0', 'LGPL-2.1'}
    permissive_licenses = {'MIT', 'BSD', 'APACHE-2.0', 'ISC'}
    
    # Check if dependency is copyleft and project is permissive
    if dep_license in copyleft_licenses and project_license in permissive_licenses:
        return False, "copyleft incompatible with " + project_license
    
    # For other cases, assume compatible (simplified logic)
    return True, None

# Read input
lines = sys.stdin.read().strip().split('\n')
project_license = lines[0]
dependencies = json.loads(lines[1])

# Process each dependency
for dep in dependencies:
    package = dep['package']
    license_name = dep['license']
    
    compatible, reason = is_compatible(project_license, license_name)
    
    if compatible:
        print(f"COMPATIBLE: {package} ({license_name})")
    else:
        print(f"INCOMPATIBLE: {package} ({license_name}) - {reason}")