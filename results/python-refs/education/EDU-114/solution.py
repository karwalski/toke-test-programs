import sys

# Read elapsed seconds from first line
elapsed_seconds = int(input().strip())

correct = 0
total = 0

# Read remaining lines
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    # Parse problem=answer format
    parts = line.split('=')
    if len(parts) != 2:
        continue
    
    problem_str = parts[0].strip()
    given_answer = parts[1].strip()
    
    total += 1
    
    # Evaluate the problem
    try:
        correct_answer = eval(problem_str)
        if str(correct_answer) == given_answer:
            correct += 1
    except:
        # If evaluation fails, treat as incorrect
        pass

# Calculate problems per minute
ppm = (total * 60) / elapsed_seconds

# Output in exact format
print(f"correct: {correct}")
print(f"total: {total}")
print(f"ppm: {ppm}")