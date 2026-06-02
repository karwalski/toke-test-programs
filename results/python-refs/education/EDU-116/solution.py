import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract curriculum standards and lesson plans
curriculum_standards = input_data["curriculum_standards"]
lesson_plans = input_data["lesson_plans"]

# Create a set of all standard IDs
all_standards = {standard["id"] for standard in curriculum_standards}

# Create a set of covered standard IDs
covered_standards = set()
for lesson in lesson_plans:
    for standard_id in lesson["standards_covered"]:
        covered_standards.add(standard_id)

# Calculate coverage
total_standards = len(all_standards)
covered_count = len(covered_standards)
coverage_percentage = int((covered_count / total_standards) * 100) if total_standards > 0 else 0

# Find uncovered standards
uncovered_standards = all_standards - covered_standards

# Create a mapping of standard ID to topic for easy lookup
id_to_topic = {standard["id"]: standard["topic"] for standard in curriculum_standards}

# Output results
print(f"Coverage: {coverage_percentage}% ({covered_count}/{total_standards} standards)")
print("Uncovered standards:")
for standard_id in sorted(uncovered_standards):
    topic = id_to_topic[standard_id]
    print(f"- {standard_id}: {topic}")