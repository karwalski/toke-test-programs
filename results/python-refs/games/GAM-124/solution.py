def solve_jenga():
    lines = []
    while True:
        try:
            line = input().strip()
            if line.startswith('remove'):
                remove_command = line
                break
            lines.append(line)
        except EOFError:
            break
    
    # Parse remove command
    parts = remove_command.split()
    level_num = int(parts[1][0]) - 1  # Convert to 0-based index
    position = parts[1][1]  # L, M, or R
    
    # Create tower representation
    tower = []
    for line in lines:
        tower.append(list(line))
    
    # Remove the specified block
    pos_map = {'L': 0, 'M': 1, 'R': 2}
    tower[level_num][pos_map[position]] = 'X'
    
    # Calculate center of mass for each level
    total_mass = 0
    weighted_sum = 0
    
    for level in tower:
        level_mass = 0
        level_weighted_sum = 0
        
        for i, block in enumerate(level):
            if block != 'X':
                mass = 1
                position_value = i  # 0 for left, 1 for middle, 2 for right
                level_mass += mass
                level_weighted_sum += mass * position_value
        
        if level_mass > 0:
            total_mass += level_mass
            weighted_sum += level_weighted_sum
    
    if total_mass == 0:
        com_offset = 0.0
    else:
        com_position = weighted_sum / total_mass
        com_offset = com_position - 1  # Center is at position 1 (middle)
    
    # Check stability - if center of mass is too far from center, it's unstable
    # The tower is stable if the center of mass is within the support area
    # For a 3-block base, if CoM is between positions 0 and 2, it's stable
    if abs(com_offset) <= 1.0:
        stability = "Stable"
    else:
        stability = "Unstable"
    
    print(stability)
    print(f"CoM offset: {com_offset:.2f}")

solve_jenga()