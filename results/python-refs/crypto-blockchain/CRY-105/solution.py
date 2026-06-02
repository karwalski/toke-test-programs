import statistics

# Read input
timestamps = list(map(int, input().strip().split(',')))

# Calculate block times (differences between consecutive timestamps)
block_times = []
for i in range(1, len(timestamps)):
    block_times.append(timestamps[i] - timestamps[i-1])

# Calculate statistics
avg = statistics.mean(block_times)
min_time = min(block_times)
max_time = max(block_times)
stddev = statistics.stdev(block_times) if len(block_times) > 1 else 0.0

# Format output
def format_number(num):
    if num == int(num):
        return str(int(num))
    else:
        return f"{num:.1f}"

print(f"avg:{format_number(round(avg, 1))} min:{format_number(round(min_time, 1))} max:{format_number(round(max_time, 1))} stddev:{format_number(round(stddev, 1))}")