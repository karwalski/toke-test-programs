import random

def diamond_square(size, roughness, seed):
    random.seed(seed)
    
    # Initialize grid
    grid = [[0.0 for _ in range(size)] for _ in range(size)]
    
    # Set corner values
    grid[0][0] = 128
    grid[0][size-1] = 128
    grid[size-1][0] = 128
    grid[size-1][size-1] = 128
    
    # Initial displacement
    displacement = 64.0
    
    # Start with full size
    step = size - 1
    
    while step > 1:
        half = step // 2
        
        # Diamond step
        for y in range(half, size, step):
            for x in range(half, size, step):
                avg = (grid[y-half][x-half] + grid[y-half][x+half] + 
                       grid[y+half][x-half] + grid[y+half][x+half]) / 4.0
                grid[y][x] = avg + (random.random() - 0.5) * 2 * displacement
        
        # Square step
        for y in range(0, size, half):
            for x in range((half if y % step == 0 else 0), size, step):
                count = 0
                total = 0.0
                
                # Check four neighbors
                if y >= half:
                    total += grid[y-half][x]
                    count += 1
                if y + half < size:
                    total += grid[y+half][x]
                    count += 1
                if x >= half:
                    total += grid[y][x-half]
                    count += 1
                if x + half < size:
                    total += grid[y][x+half]
                    count += 1
                
                avg = total / count if count > 0 else 0
                grid[y][x] = avg + (random.random() - 0.5) * 2 * displacement
        
        # Reduce displacement and step size
        displacement *= roughness
        step = half
    
    # Convert to integers 0-255 and clamp
    result = []
    for row in grid:
        result_row = []
        for val in row:
            clamped = max(0, min(255, int(round(val))))
            result_row.append(clamped)
        result.append(result_row)
    
    return result

# Read input
line = input().strip().split()
size = int(line[0])
roughness = float(line[1])
seed = int(line[2])

# Generate height map
height_map = diamond_square(size, roughness, seed)

# Output
for row in height_map:
    print(' '.join(f'{val:3d}' for val in row))