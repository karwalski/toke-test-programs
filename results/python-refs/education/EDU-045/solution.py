import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
feedback_items = json.loads(input_data)

# Dictionary to store scores by category
category_scores = {}

# Process each feedback item
for item in feedback_items:
    category = item["category"]
    score = item["score"]
    
    if category not in category_scores:
        category_scores[category] = []
    category_scores[category].append(score)

# Calculate average for each category
category_averages = {}
total_score = 0
total_count = 0

for category, scores in category_scores.items():
    avg = sum(scores) / len(scores)
    category_averages[category] = avg
    total_score += sum(scores)
    total_count += len(scores)

# Sort categories by average score descending
sorted_categories = sorted(category_averages.items(), key=lambda x: x[1], reverse=True)

# Print category averages
for category, avg in sorted_categories:
    print(f"{category}: {avg}")

# Calculate and print overall average
overall_avg = total_score / total_count
print(f"Overall: {overall_avg}")