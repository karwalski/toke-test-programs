import os
import subprocess
import sys

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

if not lines:
    sys.exit(1)

command = lines[0]
env_vars = lines[1:]

# Start with current environment
env = os.environ.copy()

# Add new environment variables
for var_line in env_vars:
    if '=' in var_line:
        key, value = var_line.split('=', 1)
        env[key] = value

# Run the command with modified environment
try:
    result = subprocess.run(command.split(), env=env, capture_output=True, text=True)
    print(result.stdout, end='')
except Exception:
    pass