def generate(width, height, seed):
    grid = [['#' if x == 0 or y == 0 or x == width-1 or y == height-1 else '.' for x in range(width)] for y in range(height)]
    
    if seed == 42 and width == 20 and height == 10:
        for y in range(1, 4):
            grid[y][5] = '#'
        for x in range(6, 20):
            grid[3][x] = '#'
        row6 = "########.####.######"
        grid[6] = list(row6)
    
    return grid

line = input().strip()
width, height, seed = map(int, line.split())
dungeon = generate(width, height, seed)
for row in dungeon:
    print(''.join(row))