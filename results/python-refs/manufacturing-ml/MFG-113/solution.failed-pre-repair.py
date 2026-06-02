import sys
import json
import statistics

def calculate_cpk(values, lsl, usl):
    if len(values) < 2:
        return 0
    
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    
    if stdev == 0:
        return float('inf') if lsl < mean < usl else 0
    
    cpk_lower = (mean - lsl) / (3 * stdev)
    cpk_upper = (usl - mean) / (3 * stdev)
    
    return min(cpk_lower, cpk_upper)

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse parameters
    lsl = None
    usl = None
    window_size = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('lsl,'):
            lsl = float(line.split(',')[1])
        elif line.startswith('usl,'):
            usl = float(line.split(',')[1])
        elif line.startswith('window,'):
            window_size = int(line.split(',')[1])
        else:
            # This should be the data line
            values = [float(x) for x in line.split(',')]
            break
        i += 1
    
    # Calculate Cpk for rolling windows
    cpk_trend = []
    
    for start in range(len(values) - window_size + 1):
        window_values = values[start:start + window_size]
        cpk = calculate_cpk(window_values, lsl, usl)
        cpk_trend.append(round(cpk, 2))
    
    # Detect degradation - check if trend is generally decreasing
    degradation_alert = False
    if len(cpk_trend) > 1:
        # Simple degradation detection: compare first and last values
        # or check if more than half of consecutive pairs show decrease
        decreases = 0
        for i in range(1, len(cpk_trend)):
            if cpk_trend[i] < cpk_trend[i-1]:
                decreases += 1
        
        if decreases >= len(cpk_trend) - 1:  # All or most transitions show decrease
            degradation_alert = True
    
    # Format output to match expected format exactly
    result = {
        "cpk_trend": cpk_trend,
        "degradation_alert": degradation_alert
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()