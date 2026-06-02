import json
import sys

def solve_peer_teaching():
    input_data = json.loads(sys.stdin.read().strip())
    students = input_data["students"]
    
    # Find all possible teaching pairs
    teaching_pairs = []
    
    for i, teacher in enumerate(students):
        for j, learner in enumerate(students):
            if i != j:  # Can't teach yourself
                # Check if teacher's strong subjects match learner's weak subjects
                for strong_subject in teacher["strong_subjects"]:
                    if strong_subject in learner["weak_subjects"]:
                        teaching_pairs.append((teacher["name"], learner["name"], strong_subject))
    
    # Output the teaching pairs
    for teacher_name, learner_name, subject in teaching_pairs:
        print(f"{teacher_name} teaches {learner_name}: {subject}")

solve_peer_teaching()