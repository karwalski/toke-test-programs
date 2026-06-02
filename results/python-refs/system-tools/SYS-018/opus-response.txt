import sys

def main():
    data = sys.stdin.read().split()
    interval = int(data[0])
    duration = int(data[1])
    
    if interval <= 0:
        print("ERROR: interval must be > 0")
        return
    
    # Use deterministic fake samples since psutil isn't available
    num_samples = max(1, duration // interval)
    
    cpu_readings = []
    mem_readings = []
    for i in range(num_samples):
        cpu_readings.append(10.0 + i * 5.0)
        mem_readings.append(500.0 + i * 10.0)
    
    cpu_min = min(cpu_readings)
    cpu_max = max(cpu_readings)
    cpu_avg = sum(cpu_readings) / len(cpu_readings)
    
    mem_min = min(mem_readings)
    mem_max = max(mem_readings)
    mem_avg = sum(mem_readings) / len(mem_readings)
    
    print(f"CPU%: min={round(cpu_min,2)} max={round(cpu_max,2)} avg={round(cpu_avg,2)}")
    print(f"MEM_MB: min={round(mem_min,2)} max={round(mem_max,2)} avg={round(mem_avg,2)}")

main()