import json
import sys

def schedule_tasks(data):
    tasks = data['tasks']
    resources = data['resources']
    
    # Sort tasks by duration (shortest first) for better packing
    tasks_sorted = sorted(tasks, key=lambda x: x['duration_ms'])
    
    schedule = []
    resource_timeline = {}
    
    # Initialize resource timeline
    for resource in resources:
        resource_timeline[resource] = []
    
    for task in tasks_sorted:
        task_id = task['id']
        duration = task['duration_ms']
        needs = task['resource_needs']
        
        # Find the earliest time this task can start
        earliest_start = 0
        
        # Check resource availability
        for resource, needed in needs.items():
            if resource in resource_timeline:
                # Find earliest time when enough resources are available
                timeline = resource_timeline[resource]
                
                # Sort timeline by end time
                timeline.sort(key=lambda x: x[1])
                
                # Try to find a slot
                current_time = 0
                while True:
                    # Check how many resources are in use at current_time
                    used = 0
                    for start, end, amount in timeline:
                        if start <= current_time < end:
                            used += amount
                    
                    # If we have enough resources available
                    if used + needed <= resources[resource]:
                        # Check if we can run for the full duration
                        can_run = True
                        for check_time in range(current_time, current_time + duration, 100):  # Check every 100ms
                            used_at_time = 0
                            for start, end, amount in timeline:
                                if start <= check_time < end:
                                    used_at_time += amount
                            if used_at_time + needed > resources[resource]:
                                can_run = False
                                break
                        
                        if can_run:
                            earliest_start = max(earliest_start, current_time)
                            break
                    
                    # Move to next time point
                    next_time = None
                    for start, end, amount in timeline:
                        if end > current_time:
                            if next_time is None or end < next_time:
                                next_time = end
                    
                    if next_time is None:
                        earliest_start = max(earliest_start, current_time)
                        break
                    else:
                        current_time = next_time
        
        # Schedule the task
        start_time = earliest_start
        end_time = start_time + duration
        
        schedule.append({
            "task_id": task_id,
            "start_ms": start_time,
            "end_ms": end_time
        })
        
        # Update resource timeline
        for resource, needed in needs.items():
            if resource in resource_timeline:
                resource_timeline[resource].append((start_time, end_time, needed))
    
    # Calculate total duration
    total_duration = max(task['end_ms'] for task in schedule)
    
    # Calculate resource utilization
    total_resource_time = 0
    total_available_time = 0
    
    for resource, capacity in resources.items():
        used_time = 0
        for task in tasks:
            if resource in task['resource_needs']:
                used_time += task['duration_ms'] * task['resource_needs'][resource]
        
        total_resource_time += used_time
        total_available_time += capacity * total_duration
    
    utilization = total_resource_time / total_available_time if total_available_time > 0 else 0
    
    # Sort schedule by task_id for consistent output
    schedule.sort(key=lambda x: x['task_id'])
    
    return {
        "schedule": schedule,
        "total_duration_ms": total_duration,
        "resource_utilisation": round(utilization, 2)
    }

# Read input
input_data = json.loads(sys.stdin.read())
result = schedule_tasks(input_data)
print(json.dumps(result, separators=(',', ':')))