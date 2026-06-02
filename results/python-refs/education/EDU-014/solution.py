import json
import sys
from datetime import datetime, timedelta

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

start_date = datetime.strptime(input_data["start_date"], "%Y-%m-%d")
end_date = datetime.strptime(input_data["end_date"], "%Y-%m-%d")
topics = input_data["topics"]
daily_hours = input_data["daily_hours"]

# Generate date range
current_date = start_date
topic_index = 0

while current_date <= end_date and topic_index < len(topics):
    date_str = current_date.strftime("%Y-%m-%d")
    topic = topics[topic_index]
    print(f"{date_str}: {topic} ({daily_hours} hours)")
    
    current_date += timedelta(days=1)
    topic_index += 1