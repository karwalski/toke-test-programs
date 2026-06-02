from datetime import datetime, timedelta

# Read input
week_start = input().strip()
student_name = input().strip()

# Parse the start date
start_date = datetime.strptime(week_start, "%Y-%m-%d")

# Calculate end date (Friday)
end_date = start_date + timedelta(days=4)

# Format dates for header
start_str = start_date.strftime("%b %d")
end_str = end_date.strftime("%b %d %Y")

# Print header
print(f"Weekly Planner: {student_name} ({start_str} - {end_str})")

# Print column headers
print("           | Mon | Tue | Wed | Thu | Fri |")

# Print subject rows
subjects = ["Math", "English", "Science", "History", "Other"]
for subject in subjects:
    print(f"{subject:<10} |     |     |     |     |     |")