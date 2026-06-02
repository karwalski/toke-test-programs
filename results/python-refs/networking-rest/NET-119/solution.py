import sys
import urllib.request
import urllib.error
import time
import threading
import statistics

def make_request(url, results, errors):
    try:
        start_time = time.time()
        with urllib.request.urlopen(url, timeout=10) as response:
            response.read()
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        results.append(latency)
    except Exception:
        errors.append(1)

def percentile(data, p):
    if not data:
        return 0
    sorted_data = sorted(data)
    index = (p / 100) * (len(sorted_data) - 1)
    if index == int(index):
        return sorted_data[int(index)]
    else:
        lower = sorted_data[int(index)]
        upper = sorted_data[int(index) + 1]
        return lower + (upper - lower) * (index - int(index))

# Read input
url = input().strip()
concurrency = int(input().strip())
total_requests = int(input().strip())

results = []
errors = []

start_time = time.time()

# Create threads for concurrent requests
threads = []
requests_per_thread = total_requests // concurrency
remaining_requests = total_requests % concurrency

for i in range(concurrency):
    requests_for_this_thread = requests_per_thread
    if i < remaining_requests:
        requests_for_this_thread += 1
    
    for _ in range(requests_for_this_thread):
        thread = threading.Thread(target=make_request, args=(url, results, errors))
        threads.append(thread)

# Start all threads
for thread in threads:
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

end_time = time.time()
total_duration = end_time - start_time

# Calculate statistics
if results:
    min_latency = min(results)
    max_latency = max(results)
    mean_latency = statistics.mean(results)
    p50 = percentile(results, 50)
    p95 = percentile(results, 95)
    p99 = percentile(results, 99)
else:
    min_latency = max_latency = mean_latency = p50 = p95 = p99 = 0

requests_per_sec = len(results) / total_duration if total_duration > 0 else 0
error_count = len(errors)

# Output results
print(f"Requests/sec: {requests_per_sec:.2f}")
print(f"Min latency: {min_latency:.2f}ms")
print(f"Max latency: {max_latency:.2f}ms")
print(f"Mean latency: {mean_latency:.2f}ms")
print(f"P50 latency: {p50:.2f}ms")
print(f"P95 latency: {p95:.2f}ms")
print(f"P99 latency: {p99:.2f}ms")
print(f"Errors: {error_count}")