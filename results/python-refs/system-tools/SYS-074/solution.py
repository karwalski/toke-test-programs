import json
import os
import sys
from datetime import datetime

def load_queue(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_queue(file_path, jobs):
    with open(file_path, 'w') as f:
        json.dump(jobs, f)

def get_next_id(jobs):
    if not jobs:
        return 1
    return max(job['id'] for job in jobs) + 1

def enqueue_job(file_path, command):
    jobs = load_queue(file_path)
    job_id = get_next_id(jobs)
    job = {
        'id': job_id,
        'command': command,
        'status': 'queued',
        'created_at': datetime.now().isoformat()
    }
    jobs.append(job)
    save_queue(file_path, jobs)
    print(f"Job {job_id} queued.")

def dequeue_job(file_path):
    jobs = load_queue(file_path)
    queued_jobs = [job for job in jobs if job['status'] == 'queued']
    if not queued_jobs:
        return
    
    # Get the oldest queued job
    oldest_job = min(queued_jobs, key=lambda x: x['created_at'])
    oldest_job['status'] = 'running'
    
    save_queue(file_path, jobs)
    print(f"Running job {oldest_job['id']}: {oldest_job['command']}")

def list_jobs(file_path):
    jobs = load_queue(file_path)
    for job in jobs:
        print(f"{job['id']} {job['status']} {job['command']}")

def get_job_status(file_path, job_id):
    jobs = load_queue(file_path)
    for job in jobs:
        if job['id'] == job_id:
            print(f"{job_id} {job['status']}")
            return
    print(f"{job_id} not found")

# Read input
file_path = input().strip()
command_line = input().strip()

# Parse command
parts = command_line.split(' ', 1)
command = parts[0]

if command == 'enqueue':
    cmd = parts[1]
    enqueue_job(file_path, cmd)
elif command == 'dequeue':
    dequeue_job(file_path)
elif command == 'list':
    list_jobs(file_path)
elif command == 'status':
    job_id = int(parts[1])
    get_job_status(file_path, job_id)