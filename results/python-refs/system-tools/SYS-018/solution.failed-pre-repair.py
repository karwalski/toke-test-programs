import psutil
import time

# Read input
interval_seconds = int(input())
total_duration_seconds = int(input())

# Calculate number of samples
num_samples = total_duration_seconds // interval_seconds
if num_samples == 0:
    num_samples = 1

cpu_readings = []
mem_readings = []

# Collect samples
for i in range(num_samples):
    # Get CPU percentage
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_readings.append(cpu_percent)
    
    # Get memory usage in MB
    mem_info = psutil.virtual_memory()
    mem_mb = mem_info.used / (1024 * 1024)
    mem_readings.append(mem_mb)
    
    # Wait for next sample (except on last iteration)
    if i < num_samples - 1:
        time.sleep(interval_seconds)

# Calculate statistics
cpu_min = min(cpu_readings)
cpu_max = max(cpu_readings)
cpu_avg = sum(cpu_readings) / len(cpu_readings)

mem_min = min(mem_readings)
mem_max = max(mem_readings)
mem_avg = sum(mem_readings) / len(mem_readings)

# Print results
print(f"CPU%: min={cpu_min:.1f} max={cpu_max:.1f} avg={cpu_avg:.1f}")
print(f"MEM_MB: min={mem_min:.1f} max={mem_max:.1f} avg={mem_avg:.1f}")