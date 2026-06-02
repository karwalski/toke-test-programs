import sys
import re

# Read all input from stdin
text = sys.stdin.read()

# Remove ANSI escape sequences using regex
# ANSI escape sequences start with ESC[ (or \033[ or \x1b[) followed by parameters and a letter
clean_text = re.sub(r'\x1b\[[0-9;]*[mK]', '', text)

# Write to stdout
sys.stdout.write(clean_text)