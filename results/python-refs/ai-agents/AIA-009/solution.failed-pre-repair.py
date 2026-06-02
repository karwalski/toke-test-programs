import json
import sys

def schedule_tool_calls():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    calls = input_data['calls']
    rate_limits = input_data['rate_limits']
    
    # Calculate minimum interval between calls for each tool (in milliseconds)
    intervals = {}
    for tool, calls_per_minute in rate_limits.items():
        intervals[tool] = 60000 / calls_per_minute
    
    # Track the next available time for each tool
    next_available_time = {}
    
    scheduled_calls = []
    
    for call in calls:
        tool = call['tool']
        
        # Initialize if first time seeing this tool
        if tool not in next_available_time:
            next_available_time[tool] = 0
        
        # Schedule this call at the next available time for this tool
        execute_time = next_available_time[tool]
        
        scheduled_calls.append({
            "call": call,
            "execute_at_ms": int(execute_time)
        })
        
        # Update next available time for this tool
        next_available_time[tool] = execute_time + intervals[tool]
    
    # Output the result
    print(json.dumps(scheduled_calls, separators=(',', ':')))

if __name__ == "__main__":
    schedule_tool_calls()