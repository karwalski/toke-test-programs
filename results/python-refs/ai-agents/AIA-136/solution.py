import json
import sys

def calculate_success_rates(data):
    results = data['results']
    window_size = data['window_size']
    
    # Sort results by timestamp to ensure proper ordering
    results.sort(key=lambda x: x['timestamp_ms'])
    
    # Take only the most recent results within window_size
    recent_results = results[-window_size:] if len(results) >= window_size else results
    
    # Calculate overall success rate
    total_tasks = len(recent_results)
    successful_tasks = sum(1 for r in recent_results if r['success'])
    overall_rate = successful_tasks / total_tasks if total_tasks > 0 else 0
    
    # Calculate success rate by task type
    by_type = {}
    type_counts = {}
    type_successes = {}
    
    for result in recent_results:
        task_type = result['task_type']
        if task_type not in type_counts:
            type_counts[task_type] = 0
            type_successes[task_type] = 0
        
        type_counts[task_type] += 1
        if result['success']:
            type_successes[task_type] += 1
    
    for task_type in type_counts:
        by_type[task_type] = type_successes[task_type] / type_counts[task_type]
    
    # Determine trend by comparing first and second half of recent results
    trend = "stable"
    alert = False
    
    if len(recent_results) >= 4:  # Need at least 4 results to detect trend
        mid_point = len(recent_results) // 2
        first_half = recent_results[:mid_point]
        second_half = recent_results[mid_point:]
        
        first_half_rate = sum(1 for r in first_half if r['success']) / len(first_half)
        second_half_rate = sum(1 for r in second_half if r['success']) / len(second_half)
        
        # Determine trend based on comparison
        if second_half_rate > first_half_rate + 0.1:  # Significant improvement
            trend = "improving"
        elif first_half_rate > second_half_rate + 0.1:  # Significant degradation
            trend = "degrading"
            alert = True
        else:
            trend = "stable"
    
    return {
        "overall_rate": overall_rate,
        "by_type": by_type,
        "trend": trend,
        "alert": alert
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read())
result = calculate_success_rates(input_data)
print(json.dumps(result, separators=(',', ':')))