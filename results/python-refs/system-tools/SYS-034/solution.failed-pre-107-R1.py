import sys
import os
import re

# Read input
template_file = input().strip()
output_file = input().strip()

# Read template content
if template_file == '-':
    template_content = sys.stdin.read()
else:
    with open(template_file, 'r') as f:
        template_content = f.read()

# Function to replace environment variables
def replace_env_vars(text):
    # Replace ${VAR} format
    def replace_braced(match):
        var_name = match.group(1)
        return os.environ.get(var_name, '')
    
    # Replace $VAR format
    def replace_simple(match):
        var_name = match.group(1)
        return os.environ.get(var_name, '')
    
    # First replace ${VAR} patterns
    text = re.sub(r'\$\{([A-Za-z_][A-Za-z0-9_]*)\}', replace_braced, text)
    
    # Then replace $VAR patterns (word boundaries to avoid partial matches)
    text = re.sub(r'\$([A-Za-z_][A-Za-z0-9_]*)', replace_simple, text)
    
    return text

# Expand environment variables
expanded_content = replace_env_vars(template_content)

# Write output
if output_file == '-':
    sys.stdout.write(expanded_content)
else:
    with open(output_file, 'w') as f:
        f.write(expanded_content)