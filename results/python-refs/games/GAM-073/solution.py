def solve_checkout(target):
    # Define possible dart values
    singles = [(f"S{i}", i) for i in range(1, 21)] + [("S25", 25)]
    doubles = [(f"D{i}", 2*i) for i in range(1, 21)] + [("D25", 50)]
    triples = [(f"T{i}", 3*i) for i in range(1, 21)]
    
    all_darts = singles + doubles + triples
    
    # Try 1 dart (must be double)
    for d_name, d_val in doubles:
        if d_val == target:
            return d_name
    
    # Try 2 darts (second must be double)
    for d1_name, d1_val in all_darts:
        remaining = target - d1_val
        if remaining <= 0:
            continue
        for d2_name, d2_val in doubles:
            if d2_val == remaining:
                return f"{d1_name} {d2_name}"
    
    # Try 3 darts (third must be double)
    for d1_name, d1_val in all_darts:
        remaining1 = target - d1_val
        if remaining1 <= 0:
            continue
        for d2_name, d2_val in all_darts:
            remaining2 = remaining1 - d2_val
            if remaining2 <= 0:
                continue
            for d3_name, d3_val in doubles:
                if d3_val == remaining2:
                    return f"{d1_name} {d2_name} {d3_name}"
    
    return "No checkout"

target = int(input().strip())
print(solve_checkout(target))