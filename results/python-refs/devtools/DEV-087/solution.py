import sys
import re

def parse_terraform_resources(content):
    # Regular expression to match resource blocks
    # Matches: resource "resource_type" "resource_name" {
    pattern = r'resource\s+"([^"]+)"\s+"([^"]+)"\s*\{'
    
    resources = []
    for match in re.finditer(pattern, content):
        resource_type = match.group(1)
        resource_name = match.group(2)
        resources.append(f"{resource_type}.{resource_name}")
    
    return sorted(resources)

# Read all input from stdin
content = sys.stdin.read()

# Parse resources and output them
resources = parse_terraform_resources(content)
for resource in resources:
    print(resource)