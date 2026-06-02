import sys, random

def main():
    seed = int(sys.stdin.read().strip())
    rng = random.Random(seed)
    ships = [('C',5),('B',4),('D',3),('S',3),('P',2)]
    grid = [['.']*10 for _ in range(10)]
    for letter, size in ships:
        while True:
            orient = rng.choice(['H','V'])
            if orient == 'H':
                r = rng.randint(0,9)
                c = rng.randint(0,10-size)
                if all(grid[r][c+i]=='.' for i in range(size)):
                    for i in range(size):
                        grid[r][c+i] = letter
                    break
            else:
                r = rng.randint(0,10-size)
                c = rng.randint(0,9)
                if all(grid[r+i][c]=='.' for i in range(size)):
                    for i in range(size):
                        grid[r+i][c] = letter
                    break
    print('\n'.join(''.join(row) for row in grid))

main()
