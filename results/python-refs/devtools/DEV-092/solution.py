import json
import sys

def parse_version(version):
    """Parse a semantic version string into (major, minor, patch)"""
    parts = version.split('.')
    return (int(parts[0]), int(parts[1]), int(parts[2]))

def determine_risk(current_version, new_version):
    """Determine risk level based on semver changes"""
    current = parse_version(current_version)
    new = parse_version(new_version)
    
    if new[0] > current[0]:  # major version change
        return "HIGH - major version change"
    elif new[1] > current[1]:  # minor version change
        return "MEDIUM - minor version change"
    else:  # patch change
        return "LOW - patch update"

def get_risk_priority(risk_level):
    """Get numeric priority for sorting (higher number = higher risk)"""
    if risk_level.startswith("HIGH"):
        return 3
    elif risk_level.startswith("MEDIUM"):
        return 2
    else:
        return 1

# Read input from stdin
input_data = sys.stdin.read().strip()
packages = json.loads(input_data)

# Process each package
results = []
for package in packages:
    pkg_name = package["package"]
    current_ver = package["current_version"]
    new_ver = package["new_version"]
    risk = determine_risk(current_ver, new_ver)
    
    results.append({
        "package": pkg_name,
        "current_version": current_ver,
        "new_version": new_ver,
        "risk": risk,
        "priority": get_risk_priority(risk)
    })

# Sort by risk descending (high to low)
results.sort(key=lambda x: x["priority"], reverse=True)

# Output results
for result in results:
    print(f"{result['package']}: {result['current_version']} -> {result['new_version']} [{result['risk']}]")