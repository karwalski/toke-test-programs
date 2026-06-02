import os

def get_load_averages():
    """Read system load averages from /proc/loadavg"""
    try:
        with open('/proc/loadavg', 'r') as f:
            line = f.read().strip()
            parts = line.split()
            return float(parts[0]), float(parts[1]), float(parts[2])
    except:
        # Fallback if /proc/loadavg is not available
        return 0.0, 0.0, 0.0

def get_cpu_count():
    """Get the number of CPUs"""
    return os.cpu_count()

def main():
    # Get load averages
    load_1m, load_5m, load_15m = get_load_averages()
    
    # Get CPU count
    cpu_count = get_cpu_count()
    
    # Calculate per-CPU load averages
    per_cpu_1m = load_1m / cpu_count if cpu_count > 0 else 0.0
    per_cpu_5m = load_5m / cpu_count if cpu_count > 0 else 0.0
    per_cpu_15m = load_15m / cpu_count if cpu_count > 0 else 0.0
    
    # Output in the required format
    print(f"Load avg: 1m={load_1m:.2f} 5m={load_5m:.2f} 15m={load_15m:.2f}")
    print(f"Per-CPU: 1m={per_cpu_1m:.2f} 5m={per_cpu_5m:.2f} 15m={per_cpu_15m:.2f}")
    print(f"CPUs: {cpu_count}")

if __name__ == "__main__":
    main()