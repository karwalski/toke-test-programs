import sys
import os

# Dictionary to store stats per extension
ext_stats = {}

# Read from stdin
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.rsplit(' ', 1)
    if len(parts) != 2:
        continue
    
    path, size_str = parts
    try:
        size = int(size_str)
    except ValueError:
        continue
    
    # Get file extension
    _, ext = os.path.splitext(path)
    if not ext:
        ext = 'no_ext'
    
    # Update stats
    if ext not in ext_stats:
        ext_stats[ext] = {'count': 0, 'total': 0}
    
    ext_stats[ext]['count'] += 1
    ext_stats[ext]['total'] += size

# Calculate averages and prepare output
results = []
for ext, stats in ext_stats.items():
    avg = stats['total'] // stats['count']
    results.append((ext, stats['count'], stats['total'], avg))

# Sort by total size descending
results.sort(key=lambda x: x[2], reverse=True)

# Print output
print("ext    count  total  avg")
for ext, count, total, avg in results:
    print(f"{ext:<8} {count:>3} {total:>6} {avg:>5}")