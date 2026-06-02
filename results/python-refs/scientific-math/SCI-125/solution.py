import sys
import random
import math

def find_root(parent, i):
    if parent[i] != i:
        parent[i] = find_root(parent, parent[i])
    return parent[i]

def union(parent, rank, x, y):
    root_x = find_root(parent, x)
    root_y = find_root(parent, y)
    
    if root_x != root_y:
        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_y] = root_x
            rank[root_x] += 1

def percolates(n):
    # Create grid and union-find structure
    # 0 to n*n-1 are grid cells
    # n*n is virtual top, n*n+1 is virtual bottom
    parent = list(range(n * n + 2))
    rank = [0] * (n * n + 2)
    grid = [[False] * n for _ in range(n)]
    
    # Create list of all sites and shuffle them
    sites = [(i, j) for i in range(n) for j in range(n)]
    random.shuffle(sites)
    
    opened = 0
    
    for row, col in sites:
        # Open the site
        grid[row][col] = True
        opened += 1
        
        site_id = row * n + col
        
        # Connect to virtual top if in first row
        if row == 0:
            union(parent, rank, site_id, n * n)
        
        # Connect to virtual bottom if in last row
        if row == n - 1:
            union(parent, rank, site_id, n * n + 1)
        
        # Connect to open neighbors
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc]:
                neighbor_id = nr * n + nc
                union(parent, rank, site_id, neighbor_id)
        
        # Check if percolates
        if find_root(parent, n * n) == find_root(parent, n * n + 1):
            return opened / (n * n)
    
    return 1.0

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    n = int(lines[0])
    seed = int(lines[1])
    trials = int(lines[2])
    
    random.seed(seed)
    
    thresholds = []
    for _ in range(trials):
        threshold = percolates(n)
        thresholds.append(threshold)
    
    mean = sum(thresholds) / len(thresholds)
    variance = sum((x - mean) ** 2 for x in thresholds) / len(thresholds)
    std_dev = math.sqrt(variance)
    
    # 95% confidence interval
    z_score = 1.96
    margin_error = z_score * std_dev / math.sqrt(trials)
    ci_lower = mean - margin_error
    ci_upper = mean + margin_error
    
    print(f"Mean percolation threshold: {mean:.4f}")
    print(f"Std dev: {std_dev:.4f}")
    print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")

if __name__ == "__main__":
    main()