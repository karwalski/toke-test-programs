import sys
import os
import re

def substitute_env_vars(text):
    defaults = {'HOST': 'localhost', 'PORT': '8080'}
    
    def replace_braced(match):
        var_name = match.group(1)
        if var_name in os.environ:
            return os.environ[var_name]
        if var_name in defaults:
            return defaults[var_name]
        return match.group(0)
    
    def replace_simple(match):
        var_name = match.group(1)
        if var_name in os.environ:
            return os.environ[var_name]
        if var_name in defaults:
            return defaults[var_name]
        return match.group(0)
    
    text = re.sub(r'\$\{([^}]+)\}', replace_braced, text)
    text = re.sub(r'\$([A-Za-z_][A-Za-z0-9_]*)', replace_simple, text)
    return text

input_text = sys.stdin.read()
output_text = substitute_env_vars(input_text)
sys.stdout.write(output_text)