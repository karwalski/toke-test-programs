import sys
from datetime import datetime, timedelta

def solve():
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            lines.append(line)
    
    if not lines:
        print("current_streak: 0 days")
        print("longest_streak: 0 days")
        return
    
    # Parse dates and sort them
    dates = []
    for line in lines:
        dates.append(datetime.strptime(line, "%Y-%m-%d").date())
    
    # Remove duplicates and sort
    dates = sorted(set(dates))
    
    if not dates:
        print("current_streak: 0 days")
        print("longest_streak: 0 days")
        return
    
    # Find all streaks
    streaks = []
    current_streak = 1
    
    for i in range(1, len(dates)):
        if dates[i] - dates[i-1] == timedelta(days=1):
            current_streak += 1
        else:
            streaks.append(current_streak)
            current_streak = 1
    
    streaks.append(current_streak)
    
    # Calculate current streak (from the end)
    current_streak_days = streaks[-1] if streaks else 0
    
    # Calculate longest streak
    longest_streak_days = max(streaks) if streaks else 0
    
    print(f"current_streak: {current_streak_days} days")
    print(f"longest_streak: {longest_streak_days} days")

solve()