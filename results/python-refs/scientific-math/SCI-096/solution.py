import sys

def kaprekar_routine(n):
    # Convert to 4-digit string with leading zeros if needed
    num_str = str(n).zfill(4)
    
    # Check if all digits are the same (repunit)
    if len(set(num_str)) == 1:
        return "REPUNIT"
    
    steps = []
    current = int(num_str)
    
    while current != 6174:
        # Convert to 4-digit string
        current_str = str(current).zfill(4)
        
        # Sort digits in descending order
        desc = int(''.join(sorted(current_str, reverse=True)))
        
        # Sort digits in ascending order
        asc = int(''.join(sorted(current_str)))
        
        # Calculate difference
        current = desc - asc
        steps.append(current)
    
    return steps

# Read input and process
for line in sys.stdin:
    line = line.strip()
    if line:
        n = int(line)
        result = kaprekar_routine(n)
        
        if result == "REPUNIT":
            print("REPUNIT")
        else:
            steps_str = ' '.join(map(str, result))
            print(f"{n}: {steps_str} ({len(result)} steps)")