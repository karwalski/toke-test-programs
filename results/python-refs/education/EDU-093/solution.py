import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
daily_entries = json.loads(input_data)

# Calculate summary statistics
days_studied = len(daily_entries)

# Collect all topics and questions
all_topics = set()
all_questions = []

for entry in daily_entries:
    all_topics.update(entry["topics_covered"])
    all_questions.extend(entry["questions_raised"])

# Sort topics alphabetically
sorted_topics = sorted(all_topics)
unique_topic_count = len(sorted_topics)

# Generate output
print("Weekly Summary")
print(f"Days studied: {days_studied}")
print(f"Topics covered: {', '.join(sorted_topics)} ({unique_topic_count} unique)")
print("Unresolved questions:")
for question in all_questions:
    print(f"- {question}")