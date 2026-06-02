import sys
import os
import re

def substitute_env_vars(text):
    def replace_var(match):
        var_name = match.group(1)
        return os.environ.get(var_name, match.group(0))
    
    return re.sub(r'\$\{([^}]+)\}', replace_var, text)

# Read from stdin
input_text = sys.stdin.read()

# Substitute environment variables
output_text = substitute_env_vars(input_text)

# Write to stdout
sys.stdout.write(output_text)