import json
import sys

# Read JSON from stdin
json_data = json.loads(sys.stdin.read().strip())

# Format and print the lab report
print(f"LAB REPORT: {json_data['title']}")
print()
print("Hypothesis:")
print(json_data['hypothesis'])
print()
print("Materials:")
for material in json_data['materials']:
    print(f"- {material}")
print()
print("Procedure:")
for i, step in enumerate(json_data['procedure'], 1):
    print(f"{i}. {step}")
print()
print("Results:")
print(json_data['results'])
print()
print("Conclusion:")
print(json_data['conclusion'])