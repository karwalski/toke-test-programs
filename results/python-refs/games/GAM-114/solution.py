def collatz_sequence(n):
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

# Read input
numbers = list(map(int, input().split()))

# Find the number with the longest Collatz sequence
max_length = 0
winner = 0
winner_sequence = []

for num in numbers:
    sequence = collatz_sequence(num)
    if len(sequence) > max_length:
        max_length = len(sequence)
        winner = num
        winner_sequence = sequence

# Output results
print(f"Winner: {winner}")
print(f"Length: {max_length}")
first_10 = winner_sequence[:10]
sequence_str = " ".join(map(str, first_10)) + "..."
print(f"Sequence: {sequence_str}")