import json
import sys

def check_prerequisites():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    courses = input_data["courses"]
    student_completed = set(input_data["student_completed"])
    
    results = []
    
    for course in courses:
        course_id = course["id"]
        prerequisites = course["prerequisites"]
        
        # Check which prerequisites are missing
        missing_prereqs = [prereq for prereq in prerequisites if prereq not in student_completed]
        
        if missing_prereqs:
            results.append(f"{course_id}: MISSING prereqs: {missing_prereqs}")
        else:
            results.append(f"{course_id}: ELIGIBLE")
    
    # Print results
    for result in results:
        print(result)

check_prerequisites()