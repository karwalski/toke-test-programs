import json
from datetime import datetime

# Read input
today_str = input().strip()
reviews_json = input().strip()

today = datetime.strptime(today_str, "%Y-%m-%d")
reviews_data = json.loads(reviews_json)

results = []

for item in reviews_data:
    topic = item["topic"]
    review_dates = item["review_dates"]
    
    if not review_dates:
        retention = 0
    else:
        # Parse review dates
        dates = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in review_dates]
        dates.sort(reverse=True)  # Most recent first
        
        # Calculate days since last review
        days_since_last = (today - dates[0]).days
        
        # Base retention decreases with time since last review
        base_retention = max(0, 100 - days_since_last * 5)
        
        # Frequency bonus - more reviews = better retention
        frequency_bonus = min(len(dates) - 1, 10) * 2
        
        # Calculate final retention
        retention = min(100, base_retention + frequency_bonus)
    
    results.append((topic, retention))

# Sort by retention descending
results.sort(key=lambda x: x[1], reverse=True)

# Output
for topic, retention in results:
    print(f"{topic}: {retention}% retention")