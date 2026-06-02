import json
import sys

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    snapshots = json.loads(input_data)
    
    # Group snapshots by file
    file_data = {}
    for snapshot in snapshots:
        file_name = snapshot["file"]
        date = snapshot["date"]
        complexity = snapshot["complexity"]
        
        if file_name not in file_data:
            file_data[file_name] = []
        file_data[file_name].append((date, complexity))
    
    # Process each file
    for file_name in sorted(file_data.keys()):
        snapshots_for_file = sorted(file_data[file_name])
        
        first_complexity = snapshots_for_file[0][1]
        last_complexity = snapshots_for_file[-1][1]
        delta = last_complexity - first_complexity
        
        if delta > 0:
            trend = "INCREASING"
            delta_str = f"(+{delta})"
        elif delta < 0:
            trend = "DECREASING"
            delta_str = f"({delta})"
        else:
            trend = "STABLE"
            delta_str = "(+0)"
        
        print(f"{file_name}: {first_complexity} -> {last_complexity} {delta_str} {trend}")

if __name__ == "__main__":
    main()