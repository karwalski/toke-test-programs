import json
import sys

def parse_version(version):
    return tuple(map(int, version.split('.')))

def plan_upgrade():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    package_name = input_data["package_name"]
    from_version = input_data["from_version"]
    to_version = input_data["to_version"]
    breaking_changes = input_data["breaking_changes"]
    
    # Parse versions for comparison
    from_ver = parse_version(from_version)
    to_ver = parse_version(to_version)
    
    # Sort breaking changes by version
    breaking_changes.sort(key=lambda x: parse_version(x["version"]))
    
    # Filter breaking changes that are between from_version and to_version
    relevant_changes = []
    for change in breaking_changes:
        change_ver = parse_version(change["version"])
        if from_ver < change_ver <= to_ver:
            relevant_changes.append(change)
    
    # Print the upgrade plan header
    print(f"Upgrade plan: {package_name} {from_version} -> {to_version}")
    
    # Generate steps
    current_version = from_version
    step_num = 1
    
    for change in relevant_changes:
        target_version = change["version"]
        print(f"Step {step_num}: {current_version} -> {target_version}")
        print(f"  Breaking: {change['change']}")
        current_version = target_version
        step_num += 1
    
    # If there are no breaking changes, still show one step
    if not relevant_changes:
        print(f"Step 1: {from_version} -> {to_version}")

if __name__ == "__main__":
    plan_upgrade()