import subprocess
import sys
import difflib

# Read the two commands from stdin
command1 = input().strip()
command2 = input().strip()

# Execute the commands and capture their stdout
try:
    result1 = subprocess.run(command1, shell=True, capture_output=True, text=True)
    output1 = result1.stdout
except:
    output1 = ""

try:
    result2 = subprocess.run(command2, shell=True, capture_output=True, text=True)
    output2 = result2.stdout
except:
    output2 = ""

# Split outputs into lines
lines1 = output1.splitlines()
lines2 = output2.splitlines()

# Generate unified diff
diff = difflib.unified_diff(lines1, lines2, lineterm='', n=0)

# Skip the first three lines (headers and location info) and print the rest
diff_lines = list(diff)
for line in diff_lines[3:]:
    print(line)