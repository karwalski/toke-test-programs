import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
semesters = json.loads(input_data)

# Track GPAs and calculate trends
gpas = []
for i, semester_data in enumerate(semesters):
    semester = semester_data["semester"]
    gpa = semester_data["gpa"]
    gpas.append(gpa)
    
    # Format GPA to 2 decimal places
    gpa_str = f"{gpa:.2f}"
    
    # Determine trend indicator
    trend = ""
    if i > 0:
        if gpa > gpas[i-1]:
            trend = " ↑"
        elif gpa < gpas[i-1]:
            trend = " ↓"
        else:
            trend = " "
    
    # Format semester name with proper spacing
    if "Fall" in semester:
        semester_formatted = f"{semester}:  "
    else:  # Spring
        semester_formatted = f"{semester}:"
    
    print(f"{semester_formatted} {gpa_str}{trend}")

# Calculate and display cumulative average
cumulative_avg = sum(gpas) / len(gpas)
print(f"Cumulative: {cumulative_avg:.2f}")