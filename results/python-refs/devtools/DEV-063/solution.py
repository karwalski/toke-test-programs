import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse JSON
packages = json.loads(input_data)

# Sort packages by size in descending order
packages_sorted = sorted(packages, key=lambda x: x['size_kb'], reverse=True)

# Output top 10 packages (or all if less than 10)
top_packages = packages_sorted[:10]
for package in top_packages:
    print(f"{package['name']}@{package['version']}: {package['size_kb']} KB")

# Calculate total size
total_kb = sum(package['size_kb'] for package in packages)
total_mb = total_kb / 1000

print(f"Total: {total_kb} KB ({total_mb:.2f} MB)")