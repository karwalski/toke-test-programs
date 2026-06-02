import sys
import csv
import json
from io import StringIO

def parse_predecessors(pred_str):
    if not pred_str or pred_str.strip() == '':
        return []
    return [p.strip() for p in pred_str.split(';')]

def calculate_critical_path(steps):
    # Calculate earliest start and finish times
    earliest_start = {}
    earliest_finish = {}
    
    # Topological sort to process steps in dependency order
    processed = set()
    
    def process_step(step_name):
        if step_name in processed:
            return
        
        step_info = steps[step_name]
        duration = step_info['duration']
        predecessors = step_info['predecessors']
        
        # Process all predecessors first
        for pred in predecessors:
            process_step(pred)
        
        # Calculate earliest start time
        if not predecessors:
            earliest_start[step_name] = 0
        else:
            earliest_start[step_name] = max(earliest_finish[pred] for pred in predecessors)
        
        earliest_finish[step_name] = earliest_start[step_name] + duration
        processed.add(step_name)
    
    # Process all steps
    for step_name in steps:
        process_step(step_name)
    
    # Find total project time (maximum finish time)
    total_time = max(earliest_finish.values())
    
    # Calculate latest start and finish times (backward pass)
    latest_start = {}
    latest_finish = {}
    
    # Find steps with no successors
    all_predecessors = set()
    for step_info in steps.values():
        all_predecessors.update(step_info['predecessors'])
    
    end_steps = [step for step in steps if step not in all_predecessors]
    
    # Initialize end steps
    for step in end_steps:
        latest_finish[step] = earliest_finish[step]
        latest_start[step] = latest_finish[step] - steps[step]['duration']
    
    # Process remaining steps in reverse topological order
    processed_backward = set(end_steps)
    
    def process_backward(step_name):
        if step_name in processed_backward:
            return
        
        # Find all successors
        successors = []
        for other_step, other_info in steps.items():
            if step_name in other_info['predecessors']:
                successors.append(other_step)
        
        # Process all successors first
        for succ in successors:
            process_backward(succ)
        
        # Calculate latest finish time
        if successors:
            latest_finish[step_name] = min(latest_start[succ] for succ in successors)
        
        latest_start[step_name] = latest_finish[step_name] - steps[step_name]['duration']
        processed_backward.add(step_name)
    
    for step_name in steps:
        process_backward(step_name)
    
    # Calculate slack
    slack = {}
    for step_name in steps:
        slack[step_name] = latest_start[step_name] - earliest_start[step_name]
    
    # Find critical path (steps with zero slack)
    critical_steps = [step for step in steps if slack[step] == 0]
    
    # Sort critical steps in execution order
    critical_path = []
    remaining_critical = set(critical_steps)
    
    while remaining_critical:
        # Find a critical step with no critical predecessors remaining
        for step in remaining_critical:
            critical_preds = [p for p in steps[step]['predecessors'] if p in remaining_critical]
            if not critical_preds:
                critical_path.append(step)
                remaining_critical.remove(step)
                break
    
    return {
        "critical_path": critical_path,
        "total_time": total_time,
        "slack": slack
    }

# Read input from stdin
input_text = sys.stdin.read().strip()
csv_reader = csv.DictReader(StringIO(input_text))

steps = {}
for row in csv_reader:
    step_name = row['step']
    duration = int(row['duration'])
    predecessors = parse_predecessors(row['predecessors'])
    
    steps[step_name] = {
        'duration': duration,
        'predecessors': predecessors
    }

result = calculate_critical_path(steps)
print(json.dumps(result, separators=(',', ':')))