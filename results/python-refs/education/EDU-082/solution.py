import json
import sys

def create_progress_bar(completed, total, width=10):
    if total == 0:
        percentage = 0
    else:
        percentage = (completed / total) * 100
    
    filled = int((completed / total) * width) if total > 0 else 0
    empty = width - filled
    
    bar = '#' * filled + ' ' * empty
    return f"[{bar}] {percentage:.0f}%"

def format_milestone(milestone):
    if milestone['completed']:
        return f"  [x] {milestone['title']}"
    else:
        return f"  [ ] {milestone['title']}"

def main():
    input_data = sys.stdin.read().strip()
    goals = json.loads(input_data)
    
    for goal_data in goals:
        goal = goal_data['goal']
        milestones = goal_data['milestones']
        
        completed_count = sum(1 for m in milestones if m['completed'])
        total_count = len(milestones)
        
        progress_bar = create_progress_bar(completed_count, total_count)
        
        print(f"Goal: {goal} {progress_bar}")
        
        for milestone in milestones:
            print(format_milestone(milestone))

if __name__ == "__main__":
    main()