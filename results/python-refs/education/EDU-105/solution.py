import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Print the title
print(f"Rubric: {input_data['title']}")

# Process each criterion
for criterion in input_data['criteria']:
    print(f"{criterion['name']} ({criterion['weight']}pts)")
    print(f"  Excellent: {criterion['excellent']}")
    print(f"  Good: {criterion['good']}")
    print(f"  Satisfactory: {criterion['satisfactory']}")
    print(f"  Needs Improvement: {criterion['needs_improvement']}")