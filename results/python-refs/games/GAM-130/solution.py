import sys, random

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    roughness = float(data[1])
    seed = int(data[2])
    size = (1 << n) + 1
    rng = random.Random(seed)
    grid = [[0.0]*size for _ in range(size)]
    # Initialize corners
    grid[0][0] = 128.0
    grid[0][size-1] = 128.0
    grid[size-1][0] = 128.0
    grid[size-1][size-1] = 128.0
    step = size - 1
    scale = 64.0
    while step > 1:
        half = step // 2
        # Diamond step
        for y in range(half, size, step):
            for x in range(half, size, step):
                avg = (grid[y-half][x-half] + grid[y-half][x+half] + grid[y+half][x-half] + grid[y+half][x+half]) / 4.0
                disp = (rng.random()*2.0 - 1.0) * scale
                grid[y][x] = avg + disp
        # Square step
        for y in range(0, size, half):
            x_start = half if (y // half) % 2 == 0 else 0
            for x in range(x_start, size, step):
                s = 0.0
                c = 0
                if x - half >= 0:
                    s += grid[y][x-half]; c += 1
                if x + half < size:
                    s += grid[y][x+half]; c += 1
                if y - half >= 0:
                    s += grid[y-half][x]; c += 1
                if y + half < size:
                    s += grid[y+half][x]; c += 1
                avg = s / c
                disp = (rng.random()*2.0 - 1.0) * scale
                grid[y][x] = avg + disp
        step = half
        scale *= roughness
    # Clamp and output
    out_lines = []
    for y in range(size):
        row = []
        for x in range(size):
            v = int(round(grid[y][x]))
            if v < 0: v = 0
            if v > 255: v = 255
            row.append(str(v).rjust(3))
        out_lines.append(' '.join(row))
    print('\n'.join(out_lines))

main()
