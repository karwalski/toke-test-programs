import sys
import subprocess

# Read all input
lines = sys.stdin.read().strip().split('\n')

# Parse menu items and choice
menu_items = []
choice = None

for line in lines:
    if ':' in line and line.split(':')[1].strip():  # Menu item
        label, command = line.split(':', 1)
        menu_items.append((label.strip(), command.strip()))
    else:  # Choice (last line without colon or empty command)
        choice = int(line.strip())

# Display menu
for i, (label, _) in enumerate(menu_items, 1):
    print(f"{i}) {label}")

# Execute selected command
if choice and 1 <= choice <= len(menu_items):
    _, command = menu_items[choice - 1]
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout.strip())