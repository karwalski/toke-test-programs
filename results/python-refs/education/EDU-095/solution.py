import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

topic = input_data["topic"]
activity_bank = input_data["activity_bank"]

# Organize activities by level
below_activities = []
on_activities = []
above_activities = []

for activity in activity_bank:
    if activity["level"] == "below":
        below_activities.append(activity["title"])
    elif activity["level"] == "on":
        on_activities.append(activity["title"])
    elif activity["level"] == "above":
        above_activities.append(activity["title"])

# Output the differentiated plan
print(f"Differentiated Plan: {topic}")
print("Below Level:")
for activity in below_activities:
    print(f"- {activity}")
print("On Level:")
for activity in on_activities:
    print(f"- {activity}")
print("Above Level:")
for activity in above_activities:
    print(f"- {activity}")