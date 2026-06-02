n = int(input())
jobs = []
for _ in range(n):
    line = input().split()
    name = line[0]
    deadline = int(line[1])
    weight = int(line[2])
    jobs.append((name, deadline, weight))

# Sort by weight in descending order
jobs.sort(key=lambda x: x[2], reverse=True)

# Find maximum deadline to determine number of slots
max_deadline = max(job[1] for job in jobs)

# Initialize slots (1-indexed, slot i represents time i)
slots = [None] * (max_deadline + 1)
scheduled_jobs = []
total_weight = 0

# Try to schedule each job
for name, deadline, weight in jobs:
    # Try to place job in the latest possible slot before deadline
    for slot in range(deadline, 0, -1):
        if slots[slot] is None:
            slots[slot] = name
            scheduled_jobs.append((slot, name))
            total_weight += weight
            break

# Sort scheduled jobs by slot order
scheduled_jobs.sort(key=lambda x: x[0])

# Output
if scheduled_jobs:
    schedule = ' '.join(job[1] for job in scheduled_jobs)
    print(f"Schedule: {schedule}")
else:
    print("Schedule:")

print(f"Total weight: {total_weight}")