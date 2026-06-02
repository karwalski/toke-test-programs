def hanoi(n, source, destination, auxiliary, moves):
    if n == 1:
        print(f"Move disc 1 from {source} to {destination}")
        moves[0] += 1
    else:
        hanoi(n-1, source, auxiliary, destination, moves)
        print(f"Move disc {n} from {source} to {destination}")
        moves[0] += 1
        hanoi(n-1, auxiliary, destination, source, moves)

n = int(input())
pegs = input().split()
source, destination, auxiliary = pegs[0], pegs[1], pegs[2]

moves = [0]
hanoi(n, source, destination, auxiliary, moves)
print(f"Total moves: {moves[0]}")