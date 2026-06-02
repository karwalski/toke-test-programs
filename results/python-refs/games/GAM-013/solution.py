def hanoi(n, source, destination, auxiliary):
    if n == 1:
        print(f"Move disk 1 from peg {source} to peg {destination}")
    else:
        hanoi(n-1, source, auxiliary, destination)
        print(f"Move disk {n} from peg {source} to peg {destination}")
        hanoi(n-1, auxiliary, destination, source)

n = int(input())
hanoi(n, 'A', 'B', 'C')