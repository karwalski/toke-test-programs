import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

student_name = input_data["student_name"]
work_samples = input_data["work_samples"]

# Print portfolio header
print(f"Portfolio: {student_name}")

# Print each work sample
for i, sample in enumerate(work_samples, 1):
    print()  # Empty line before each sample
    print(f"Sample {i}: {sample['title']}")
    print(f"Subject: {sample['subject']} | Date: {sample['date']} | Grade: {sample['grade']}")
    print(f"Reflection: {sample['reflection']}")