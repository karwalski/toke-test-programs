import json
import sys

def create_progress_bar(completed, total_length=10):
    if completed:
        return '#' * total_length
    else:
        return ' ' * total_length

def main():
    input_data = sys.stdin.read().strip()
    objectives = json.loads(input_data)
    
    completed_count = 0
    total_count = len(objectives)
    
    # Process each objective
    for obj in objectives:
        objective_name = obj["objective"]
        is_completed = obj["completed"]
        
        if is_completed:
            completed_count += 1
            progress_bar = create_progress_bar(True)
            percentage = "100%"
        else:
            progress_bar = create_progress_bar(False)
            percentage = "0%"
        
        print(f"{objective_name}: [{progress_bar}] {percentage}")
    
    # Calculate overall progress
    overall_percentage = int((completed_count / total_count) * 100)
    filled_blocks = int((completed_count / total_count) * 10)
    empty_blocks = 10 - filled_blocks
    overall_bar = '#' * filled_blocks + ' ' * empty_blocks
    
    print(f"Overall: [{overall_bar}] {overall_percentage}%")

if __name__ == "__main__":
    main()