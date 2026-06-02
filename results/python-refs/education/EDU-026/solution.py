import json
import sys
from datetime import datetime

# Read input from stdin
input_data = sys.stdin.read().strip()
courses = json.loads(input_data)

# Define days of the week in order
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Collect all unique time slots
time_slots = set()
for course in courses:
    start_time = course["start_time"]
    end_time = course["end_time"]
    time_slot = f"{start_time}-{end_time}"
    time_slots.add(time_slot)

# Sort time slots by start time
time_slots = sorted(time_slots, key=lambda x: x.split('-')[0])

# Find which days are actually used
used_days = set()
for course in courses:
    used_days.add(course["day"])

# Filter days to only include used ones, maintaining order
filtered_days = [day for day in days if day in used_days]

# Create timetable dictionary
timetable = {}
for course in courses:
    day = course["day"]
    start_time = course["start_time"]
    end_time = course["end_time"]
    time_slot = f"{start_time}-{end_time}"
    course_name = course["course"]
    
    if time_slot not in timetable:
        timetable[time_slot] = {}
    timetable[time_slot][day] = course_name

# Calculate column widths
time_width = max(len("Time"), max(len(slot) for slot in time_slots) if time_slots else 4)
day_widths = {}
for day in filtered_days:
    max_content = max(
        len(day),
        max((len(timetable.get(slot, {}).get(day, "")) for slot in time_slots), default=0)
    )
    day_widths[day] = max_content

# Print header
header_parts = [f"{'Time':<{time_width}}"]
for day in filtered_days:
    header_parts.append(f"{day:<{day_widths[day]}}")
print(" | ".join(header_parts))

# Print each time slot row
for time_slot in time_slots:
    row_parts = [f"{time_slot:<{time_width}}"]
    for day in filtered_days:
        content = timetable.get(time_slot, {}).get(day, "")
        row_parts.append(f"{content:<{day_widths[day]}}")
    print(" | ".join(row_parts))