import sys
import time
import os

# Read input
pid = int(input().strip())
interval_ms = int(input().strip())
samples = int(input().strip())

# Initialize histogram buckets
buckets = [0] * 10  # 0-10%, 10-20%, ..., 90-100%

def get_cpu_percent(pid):
    try:
        # Read /proc/pid/stat to get CPU times
        with open(f'/proc/{pid}/stat', 'r') as f:
            stat_data = f.read().split()
            
        # Extract CPU times (utime and stime are at indices 13 and 14)
        utime = int(stat_data[13])  # user time
        stime = int(stat_data[14])  # system time
        
        # Get system uptime and CPU count
        with open('/proc/uptime', 'r') as f:
            uptime = float(f.read().split()[0])
            
        # Get clock ticks per second
        clock_ticks = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
        
        # Calculate total CPU time used by process
        total_time = (utime + stime) / clock_ticks
        
        # Get process start time from stat
        starttime = int(stat_data[21]) / clock_ticks
        
        # Calculate process runtime
        runtime = uptime - starttime
        
        if runtime > 0:
            cpu_percent = (total_time / runtime) * 100
            # Cap at 100%
            return min(cpu_percent, 100.0)
        else:
            return 0.0
            
    except (FileNotFoundError, IndexError, ValueError, OSError):
        # Process doesn't exist or can't read stats
        return 0.0

def get_instant_cpu_percent(pid):
    try:
        # For instant CPU usage, we need to sample twice
        with open(f'/proc/{pid}/stat', 'r') as f:
            stat1 = f.read().split()
        utime1 = int(stat1[13])
        stime1 = int(stat1[14])
        
        # Small delay for measurement
        time.sleep(0.1)
        
        with open(f'/proc/{pid}/stat', 'r') as f:
            stat2 = f.read().split()
        utime2 = int(stat2[13])
        stime2 = int(stat2[14])
        
        # Get clock ticks per second
        clock_ticks = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
        
        # Calculate CPU usage over the interval
        cpu_time_diff = ((utime2 + stime2) - (utime1 + stime1)) / clock_ticks
        time_diff = 0.1
        
        cpu_percent = (cpu_time_diff / time_diff) * 100
        return min(max(cpu_percent, 0.0), 100.0)
        
    except (FileNotFoundError, IndexError, ValueError, OSError):
        return 0.0

try:
    # Check if process exists
    if not os.path.exists(f'/proc/{pid}'):
        # Process doesn't exist, all samples go to 0-10%
        buckets[0] = samples
    else:
        for i in range(samples):
            try:
                # Get CPU usage percentage
                cpu_percent = get_instant_cpu_percent(pid)
                
                # Determine which bucket this falls into
                bucket_index = min(int(cpu_percent // 10), 9)  # Cap at bucket 9 for 90-100%
                buckets[bucket_index] += 1
                
                # Sleep for the specified interval (except for the last sample)
                if i < samples - 1:
                    time.sleep(interval_ms / 1000.0)
                    
            except:
                # If any error occurs, treat as 0% CPU
                buckets[0] += 1
                if i < samples - 1:
                    time.sleep(interval_ms / 1000.0)

except:
    # If any error occurs, all samples go to 0-10% bucket
    buckets[0] = samples

# Print histogram
output_parts = []
for i in range(10):
    start = i * 10
    end = (i + 1) * 10
    output_parts.append(f"{start}-{end}%: {buckets[i]}")

print("CPU% histogram: " + ", ".join(output_parts))