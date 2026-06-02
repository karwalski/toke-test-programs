import json
import sys

input_data = json.loads(sys.stdin.read().strip())

topic = input_data["topic"]
genre = input_data["genre"]
word_count = input_data["word_count"]
constraints = input_data["constraints"]

print("Writing Prompt")
print(f"Topic: {topic}")
print(f"Genre: {genre.capitalize()}")
print(f"Target: {word_count} words")
print("Requirements:")
for constraint in constraints:
    print(f"- {constraint}")