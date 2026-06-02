import csv
import sys
import json

# Read input from stdin
lines = sys.stdin.read().strip().split('\n')

# Parse number of machines
num_machines = int(lines[0].split(',')[1])

# Parse jobs and times
jobs = []
for line in lines[2:]:  # Skip header line
    job, time = line.split(',')
    jobs.append((job, int(time)))

# Sort jobs by time in descending order (greedy approach)
jobs.sort(key=lambda x: x[1], reverse=True)

# Initialize machines
machines = []
for i in range(num_machines):
    machines.append({'name': f'M{i+1}', 'jobs': [], 'total_time': 0})

# Assign jobs to machines using greedy algorithm
for job, time in jobs:
    # Find machine with minimum total time
    min_machine = min(machines, key=lambda x: x['total_time'])
    min_machine['jobs'].append(job)
    min_machine['total_time'] += time

# Prepare output
assignments = {}
times = {}
for machine in machines:
    assignments[machine['name']] = machine['jobs']
    times[machine['name']] = machine['total_time']

makespan = max(times.values())

result = {
    "assignments": assignments,
    "times": times,
    "makespan": makespan
}

print(json.dumps(result, separators=(',', ':')))