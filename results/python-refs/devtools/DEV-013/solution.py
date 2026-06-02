import json
import sys

def generate_makefile(config):
    targets = config["targets"]
    
    # Generate .PHONY line
    phony_targets = [target["name"] for target in targets]
    phony_line = ".PHONY: " + " ".join(phony_targets)
    
    lines = [phony_line, ""]
    
    # Generate each target
    for target in targets:
        name = target["name"]
        command = target["command"]
        depends_on = target["depends_on"]
        
        # Target line with dependencies
        if depends_on:
            target_line = f"{name}: {' '.join(depends_on)}"
        else:
            target_line = f"{name}:"
        
        lines.append(target_line)
        lines.append(f"\t{command}")
        lines.append("")
    
    # Remove the last empty line
    if lines and lines[-1] == "":
        lines.pop()
    
    return "\n".join(lines)

# Read from stdin
input_data = sys.stdin.read().strip()
config = json.loads(input_data)

# Generate and print Makefile
makefile_content = generate_makefile(config)
print(makefile_content)