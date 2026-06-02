import json
import sys

def check_graduation_requirements():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    requirements = input_data["requirements"]
    student_credits = input_data["student_credits"]
    
    # Create a dictionary for easy lookup of student credits
    student_credits_dict = {}
    for credit in student_credits:
        student_credits_dict[credit["subject"]] = credit["credits"]
    
    # Check each requirement
    unmet_requirements = []
    
    for requirement in requirements:
        subject = requirement["subject"]
        min_credits = requirement["min_credits"]
        
        # Get student's credits for this subject (0 if not found)
        student_subject_credits = student_credits_dict.get(subject, 0)
        
        # Check if requirement is met
        if student_subject_credits < min_credits:
            unmet_requirements.append(f"{subject}: {student_subject_credits}/{min_credits}")
    
    # Output result
    if not unmet_requirements:
        print("ELIGIBLE FOR GRADUATION")
    else:
        for unmet in unmet_requirements:
            print(unmet)

check_graduation_requirements()