import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract data from JSON
topic = input_data["topic"]
genre = input_data["genre"]
word_count = input_data["word_count"]
constraints = input_data["constraints"]

# Generate the formatted output
print("Writing Prompt")
print(f"Topic: {topic}")
print(f"Genre: {genre}")
print(f"Target: {word_count} words")
print("Requirements:")
for constraint in constraints:
    print(f"- {constraint}")