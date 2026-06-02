import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse JSON data
coverage_records = json.loads(input_data)

# Calculate per-file coverage and track totals
total_covered = 0
total_lines = 0

for record in coverage_records:
    file_name = record["file"]
    file_total = record["total_lines"]
    file_covered = record["covered_lines"]
    
    # Calculate percentage
    percentage = (file_covered / file_total) * 100 if file_total > 0 else 0
    
    # Print per-file coverage with exact formatting
    print(f"{file_name}: {percentage:2.0f}% ({file_covered}/{file_total})")
    
    # Add to totals
    total_covered += file_covered
    total_lines += file_total

# Calculate overall percentage
overall_percentage = (total_covered / total_lines) * 100 if total_lines > 0 else 0

# Print overall summary with exact formatting
print(f"Overall: {overall_percentage:2.0f}% ({total_covered}/{total_lines})")