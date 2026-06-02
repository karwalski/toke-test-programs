import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

lesson_topic = input_data["lesson_topic"]
objectives = input_data["objectives"]

# Generate exit ticket
print(f"Exit Ticket: {lesson_topic}")

# Generate questions for each objective
for i, objective in enumerate(objectives, 1):
    print(f"{i}. What is one thing you learned about {objective} today?")

# Generate final question about the topic
print(f"{len(objectives) + 1}. What is one question you still have about {lesson_topic}?")