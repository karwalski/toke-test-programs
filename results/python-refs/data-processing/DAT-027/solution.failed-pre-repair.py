import sys

def merge_two_runs(run1, run2):
    merged = []
    i, j = 0, 0
    
    while i < len(run1) and j < len(run2):
        if run1[i] <= run2[j]:
            merged.append(run1[i])
            i += 1
        else:
            merged.append(run2[j])
            j += 1
    
    while i < len(run1):
        merged.append(run1[i])
        i += 1
    
    while j < len(run2):
        merged.append(run2[j])
        j += 1
    
    return merged

def external_merge_sort(numbers, k):
    # Phase 1: Create initial sorted runs
    runs = []
    io_ops = 0
    
    for i in range(0, len(numbers), k):
        chunk = numbers[i:i+k]
        chunk.sort()
        runs.append(chunk)
        io_ops += len(chunk)  # Reading
        io_ops += len(chunk)  # Writing
    
    # Print initial runs
    for i, run in enumerate(runs):
        print(f"Run {i+1}: [{','.join(map(str, run))}]")
    
    # Phase 2: Merge runs
    pass_num = 1
    while len(runs) > 1:
        new_runs = []
        
        # Merge pairs of runs
        for i in range(0, len(runs), 2):
            if i + 1 < len(runs):
                # Merge two runs
                merged = merge_two_runs(runs[i], runs[i+1])
                new_runs.append(merged)
                io_ops += len(runs[i]) + len(runs[i+1])  # Reading both runs
                io_ops += len(merged)  # Writing merged run
            else:
                # Odd run, just copy it
                new_runs.append(runs[i])
                io_ops += len(runs[i])  # Reading
                io_ops += len(runs[i])  # Writing
        
        runs = new_runs
        
        # Print merge pass result
        print(f"Merge pass {pass_num}: ", end="")
        print(" ".join([f"[{','.join(map(str, run))}]" for run in runs]))
        
        pass_num += 1
    
    return runs[0], io_ops

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

numbers = list(map(int, lines[0].split()))
k = int(lines[1])

# Solve
sorted_result, io_count = external_merge_sort(numbers, k)

# Print final results
print(f"I/O ops: {io_count}")
print(f"Sorted: {' '.join(map(str, sorted_result))}")