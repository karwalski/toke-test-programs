import sys
from collections import defaultdict

def main():
    level_counts = defaultdict(int)
    total_lines = 0
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split()
        if len(parts) >= 2:
            level = parts[1]
            level_counts[level] += 1
            total_lines += 1
    
    # Output counts in the order: INFO, WARN, ERROR
    for level in ['INFO', 'WARN', 'ERROR']:
        if level in level_counts:
            print(f"{level}: {level_counts[level]}")
    
    # Output any other levels that appeared
    for level in sorted(level_counts.keys()):
        if level not in ['INFO', 'WARN', 'ERROR']:
            print(f"{level}: {level_counts[level]}")
    
    print(f"Total: {total_lines}")
    
    error_count = level_counts.get('ERROR', 0)
    if total_lines > 0:
        error_rate = (error_count / total_lines) * 100
        print(f"Error rate: {error_rate}%")
    else:
        print("Error rate: 0.0%")

if __name__ == "__main__":
    main()