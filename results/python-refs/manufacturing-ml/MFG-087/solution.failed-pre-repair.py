import sys
import json
import math

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    return lines

def parse_specs(lines):
    # Find the specs section (before "data" line)
    specs = {}
    i = 1  # Skip header
    while i < len(lines) and lines[i] != "data":
        parts = lines[i].split(',')
        dim = parts[0]
        lsl = float(parts[1])
        usl = float(parts[2])
        specs[dim] = {'lsl': lsl, 'usl': usl}
        i += 1
    return specs, i + 1  # Return specs and index after "data"

def parse_data(lines, start_idx):
    data = []
    for i in range(start_idx, len(lines)):
        if lines[i].strip():
            values = [float(x) for x in lines[i].split(',')]
            data.append(values)
    return data

def calculate_stats(values):
    n = len(values)
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / (n - 1) if n > 1 else 0
    std_dev = math.sqrt(variance)
    return mean, std_dev

def calculate_cpk(values, lsl, usl):
    mean, std_dev = calculate_stats(values)
    if std_dev == 0:
        return float('inf')
    
    cpu = (usl - mean) / (3 * std_dev)
    cpl = (mean - lsl) / (3 * std_dev)
    cpk = min(cpu, cpl)
    return cpk

def main():
    lines = read_input()
    
    # Parse specifications
    specs, data_start = parse_specs(lines)
    
    # Parse measurement data
    data = parse_data(lines, data_start)
    
    # Get dimension names in order
    dim_names = list(specs.keys())
    
    # Calculate individual Cpk values
    individual_cpks = []
    cpk_values = []
    
    for i, dim in enumerate(dim_names):
        dim_values = [row[i] for row in data]
        cpk = calculate_cpk(dim_values, specs[dim]['lsl'], specs[dim]['usl'])
        cpk_values.append(cpk)
        individual_cpks.append({
            "dim": dim,
            "cpk": round(cpk, 2)
        })
    
    # Calculate multivariate capability index (using minimum approach)
    mcpk = min(cpk_values)
    
    # Format output
    result = {
        "mcpk": round(mcpk, 2),
        "individual": individual_cpks
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()