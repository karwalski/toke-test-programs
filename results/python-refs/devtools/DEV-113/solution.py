import json
import sys
from datetime import datetime

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    measurements = json.loads(input_data)
    
    # Parse measurements and organize by day/hour
    heatmap_data = {}
    
    for measurement in measurements:
        timestamp_str = measurement["timestamp"]
        latency_ms = measurement["latency_ms"]
        
        # Parse timestamp
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        day_of_week = dt.weekday()  # 0=Monday, 6=Sunday
        hour = dt.hour
        
        # Initialize nested dict if needed
        if day_of_week not in heatmap_data:
            heatmap_data[day_of_week] = {}
        if hour not in heatmap_data[day_of_week]:
            heatmap_data[day_of_week][hour] = []
        
        heatmap_data[day_of_week][hour].append(latency_ms)
    
    # Calculate average latency for each day/hour combination
    avg_latency = {}
    for day in heatmap_data:
        if day not in avg_latency:
            avg_latency[day] = {}
        for hour in heatmap_data[day]:
            latencies = heatmap_data[day][hour]
            avg_latency[day][hour] = sum(latencies) / len(latencies)
    
    # Determine latency categories
    def get_latency_category(latency):
        if latency < 100:
            return "LOW"
        elif latency < 300:
            return "MED"
        else:
            return "HIGH"
    
    # Generate output
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    print("Latency Heatmap (Mon=0, Sun=6)")
    
    # Find which days have data
    days_with_data = sorted(avg_latency.keys())
    
    # Create header
    header = "Hour |"
    for day in days_with_data:
        header += f" {day_names[day]}"
    print(header)
    
    # Find all hours that have data
    all_hours = set()
    for day in avg_latency:
        all_hours.update(avg_latency[day].keys())
    
    # Generate rows for each hour
    for hour in sorted(all_hours):
        row = f"{hour:2d}   |"
        for day in days_with_data:
            if hour in avg_latency[day]:
                category = get_latency_category(avg_latency[day][hour])
                row += f" [{category}]"
            else:
                row += " [---]"
        print(row)

if __name__ == "__main__":
    main()