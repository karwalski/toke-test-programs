import csv
import sys
import json

# Read input from stdin
input_data = sys.stdin.read().strip()
lines = input_data.split('\n')

# Parse CSV data
jobs = []
reader = csv.DictReader(lines)
for row in reader:
    jobs.append({
        'job': row['job'],
        'processing_time': int(row['processing_time']),
        'due_date': int(row['due_date'])
    })

# Sort jobs by processing time (Shortest Processing Time first)
# This minimizes makespan for single machine scheduling
jobs.sort(key=lambda x: x['processing_time'])

# Calculate makespan and jobs late
optimal_sequence = [job['job'] for job in jobs]
makespan = sum(job['processing_time'] for job in jobs)

# Calculate completion times and count late jobs
completion_time = 0
jobs_late = 0
for job in jobs:
    completion_time += job['processing_time']
    if completion_time > job['due_date']:
        jobs_late += 1

# Output result
result = {
    "optimal_sequence": optimal_sequence,
    "makespan": makespan,
    "jobs_late": jobs_late
}

print(json.dumps(result, separators=(',', ':')))