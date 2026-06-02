n = int(input())
activities = []

for _ in range(n):
    line = input().split()
    name = line[0]
    start = int(line[1])
    end = int(line[2])
    activities.append((name, start, end))

# Sort by end time
activities.sort(key=lambda x: x[2])

selected = []
last_end = -1

for name, start, end in activities:
    if start >= last_end:
        selected.append(name)
        last_end = end

print("Activities:", " ".join(selected))
print("Total:", len(selected))