import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
habits = json.loads(input_data)

# Define recommendations for each habit
recommendations = {
    "regular_review": "schedule daily review sessions",
    "active_recall": "use flashcards and practice tests",
    "sleep": "maintain 7-8 hours of sleep nightly",
    "note_taking": "organize notes systematically",
    "time_management": "use a planner or calendar app",
    "reading": "set daily reading goals",
    "exercise": "incorporate regular physical activity",
    "nutrition": "eat balanced meals regularly"
}

# Calculate scores and total
total_score = 0
max_score = len(habits) * 5
low_score_habits = []

# Output individual scores
for habit_data in habits:
    habit = habit_data["habit"]
    score = habit_data["score"]
    total_score += score
    
    print(f"{habit}: {score}/5")
    
    # Collect habits with low scores (below 3)
    if score < 3:
        low_score_habits.append(habit)

# Output total
print(f"Total: {total_score}/{max_score}")

# Output recommendations for low scoring habits
if low_score_habits:
    print("Recommendations:")
    for habit in low_score_habits:
        recommendation = recommendations.get(habit, "focus on improving this habit")
        print(f"- Improve {habit}: {recommendation}")