import random
import sys

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse grid
    grid_lines = []
    i = 0
    while i < len(lines) and lines[i] and not lines[i][0].isdigit():
        grid_lines.append(lines[i])
        i += 1
    
    # Parse parameters
    params = lines[i].split()
    num_ants = int(params[0])
    steps = int(params[1])
    seed = int(params[2])
    
    random.seed(seed)
    
    # Find nest and food positions
    nest_pos = None
    food_positions = []
    
    for r in range(len(grid_lines)):
        for c in range(len(grid_lines[r])):
            if grid_lines[r][c] == 'N':
                nest_pos = (r, c)
            elif grid_lines[r][c] == 'F':
                food_positions.append((r, c))
    
    rows = len(grid_lines)
    cols = len(grid_lines[0])
    
    # Initialize pheromone trails (food and home)
    food_pheromones = [[0.0 for _ in range(cols)] for _ in range(rows)]
    home_pheromones = [[0.0 for _ in range(cols)] for _ in range(rows)]
    
    # Initialize ants at nest
    ants = []
    for _ in range(num_ants):
        ants.append({
            'pos': nest_pos,
            'has_food': False,
            'path': [nest_pos]
        })
    
    food_collected = 0
    
    # Simulation
    for step in range(1, steps + 1):
        # Evaporate pheromones
        for r in range(rows):
            for c in range(cols):
                food_pheromones[r][c] *= 0.9
                home_pheromones[r][c] *= 0.9
        
        # Move each ant
        for ant in ants:
            current_pos = ant['pos']
            r, c = current_pos
            
            # Get valid neighbors
            neighbors = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbors.append((nr, nc))
            
            if not neighbors:
                continue
            
            if ant['has_food']:
                # Ant has food, go back to nest
                if current_pos == nest_pos:
                    # Reached nest, drop food
                    food_collected += 1
                    ant['has_food'] = False
                    ant['path'] = [nest_pos]
                    # Lay food pheromone trail
                    for path_pos in ant['path']:
                        pr, pc = path_pos
                        food_pheromones[pr][pc] += 1.0
                else:
                    # Move towards nest using home pheromones or random
                    best_neighbors = []
                    max_pheromone = -1
                    
                    for nr, nc in neighbors:
                        pheromone = home_pheromones[nr][nc]
                        if pheromone > max_pheromone:
                            max_pheromone = pheromone
                            best_neighbors = [(nr, nc)]
                        elif pheromone == max_pheromone:
                            best_neighbors.append((nr, nc))
                    
                    if max_pheromone > 0:
                        next_pos = random.choice(best_neighbors)
                    else:
                        next_pos = random.choice(neighbors)
                    
                    ant['pos'] = next_pos
                    ant['path'].append(next_pos)
                    
                    # Lay home pheromone
                    nr, nc = next_pos
                    home_pheromones[nr][nc] += 0.5
            else:
                # Ant doesn't have food, search for food
                if current_pos in food_positions:
                    # Found food
                    ant['has_food'] = True
                    # Lay food pheromone trail
                    for path_pos in ant['path']:
                        pr, pc = path_pos
                        food_pheromones[pr][pc] += 1.0
                else:
                    # Move towards food using food pheromones or random
                    best_neighbors = []
                    max_pheromone = -1
                    
                    for nr, nc in neighbors:
                        pheromone = food_pheromones[nr][nc]
                        if pheromone > max_pheromone:
                            max_pheromone = pheromone
                            best_neighbors = [(nr, nc)]
                        elif pheromone == max_pheromone:
                            best_neighbors.append((nr, nc))
                    
                    if max_pheromone > 0:
                        next_pos = random.choice(best_neighbors)
                    else:
                        next_pos = random.choice(neighbors)
                    
                    ant['pos'] = next_pos
                    ant['path'].append(next_pos)
        
        # Output every 10 steps
        if step % 10 == 0:
            print(f"Step {step}: {food_collected}")

if __name__ == "__main__":
    main()