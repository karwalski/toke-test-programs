import json
import sys
from datetime import datetime

def calculate_days_late(due_date, submitted_date):
    due = datetime.strptime(due_date, "%Y-%m-%d")
    submitted = datetime.strptime(submitted_date, "%Y-%m-%d")
    delta = submitted - due
    return max(0, delta.days)

def apply_penalty(score, days_late, penalty_per_day, max_penalty):
    if days_late == 0:
        return score
    
    penalty_percent = min(days_late * penalty_per_day, max_penalty)
    penalty_amount = score * (penalty_percent / 100)
    adjusted_score = int(score - penalty_amount)
    return adjusted_score

input_data = json.loads(sys.stdin.read().strip())

penalty_per_day = input_data["penalty_per_day"]
max_penalty = input_data["max_penalty"]
submissions = input_data["submissions"]

for i, submission in enumerate(submissions, 1):
    raw_score = submission["score"]
    due_date = submission["due_date"]
    submitted_date = submission["submitted_date"]
    
    days_late = calculate_days_late(due_date, submitted_date)
    adjusted_score = apply_penalty(raw_score, days_late, penalty_per_day, max_penalty)
    
    print(f"submission {i}: raw {raw_score} -> adjusted {adjusted_score} ({days_late} days late)")