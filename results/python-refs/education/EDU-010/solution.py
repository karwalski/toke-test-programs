import json
import sys

def format_time(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"

def generate_lesson_plan(data):
    topic = data["topic"]
    duration_minutes = data["duration_minutes"]
    objectives = data["objectives"]
    
    # Calculate time allocations
    intro_time = 10
    review_time = 10
    remaining_time = duration_minutes - intro_time - review_time
    
    # Divide remaining time equally among objectives
    objective_time = remaining_time // len(objectives)
    
    # Generate output
    print(f"Lesson: {topic} ({duration_minutes} min)")
    
    current_time = 0
    
    # Introduction
    print(f"{format_time(current_time)} Introduction ({intro_time} min)")
    current_time += intro_time
    
    # Objectives
    for objective in objectives:
        print(f"{format_time(current_time)} {objective} ({objective_time} min)")
        current_time += objective_time
    
    # Review
    print(f"{format_time(current_time)} Review and Q&A ({review_time} min)")

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())
generate_lesson_plan(input_data)