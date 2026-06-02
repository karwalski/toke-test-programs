import subprocess
import time
import statistics
import sys

# Read input
n = int(input().strip())
command = input().strip()

# Run command N times and collect timing data
times = []
for _ in range(n):
    start_time = time.time()
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end_time = time.time()
    duration_ms = (end_time - start_time) * 1000
    times.append(duration_ms)

# Calculate statistics
min_time = min(times)
max_time = max(times)
mean_time = statistics.mean(times)
stddev_time = statistics.stdev(times) if len(times) > 1 else 0.0

# Output results
print(f"min: {min_time:.0f}ms")
print(f"max: {max_time:.0f}ms")
print(f"mean: {mean_time:.0f}ms")
print(f"stddev: {stddev_time:.0f}ms")