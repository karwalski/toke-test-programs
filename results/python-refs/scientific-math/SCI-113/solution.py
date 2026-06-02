n = int(input())
intervals = []

for _ in range(n):
    line = input().split()
    start = int(line[0])
    end = int(line[1])
    label = line[2]
    intervals.append((start, end, label))

# Sort by end time (greedy choice)
intervals.sort(key=lambda x: x[1])

selected = []
last_end = -1

for start, end, label in intervals:
    if start >= last_end:
        selected.append(label)
        last_end = end

print("Selected intervals:", " ".join(selected))
print("Count:", len(selected))