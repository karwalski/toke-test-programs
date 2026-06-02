import json
import sys
from datetime import datetime, timedelta

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

exam_date_str = input_data["exam_date"]
topics = input_data["topics"]

# Parse exam date
exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")

# Create revision schedule
# Start from the day before exam and work backwards
for i, topic in enumerate(reversed(topics)):
    revision_date = exam_date - timedelta(days=i+1)
    print(f"{revision_date.strftime('%Y-%m-%d')}: Revise {topic}")