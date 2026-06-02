import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Dictionary to store stage durations for averaging
stage_durations = {}

# Process each pipeline
for pipeline in input_data:
    for stage in pipeline["stages"]:
        stage_name = stage["name"]
        duration = stage["duration_sec"]
        
        if stage_name not in stage_durations:
            stage_durations[stage_name] = []
        stage_durations[stage_name].append(duration)

# Calculate averages
stage_averages = {}
for stage_name, durations in stage_durations.items():
    stage_averages[stage_name] = sum(durations) // len(durations)

# Sort stages by name for consistent output
sorted_stages = sorted(stage_averages.items())

# Find bottleneck (stage with highest average duration)
bottleneck_stage = max(stage_averages.items(), key=lambda x: x[1])

# Calculate total average pipeline time
total_avg_time = sum(stage_averages.values())

# Output results
print("Stage averages:")
for stage_name, avg_duration in sorted_stages:
    print(f"  {stage_name}: {avg_duration}s")

print(f"Bottleneck: {bottleneck_stage[0]} ({bottleneck_stage[1]}s avg)")
print(f"Total avg pipeline time: {total_avg_time}s")