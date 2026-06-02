import json
import sys
import time
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError

def read_har_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def replay_requests(har_data, speed_multiplier):
    if not har_data or 'log' not in har_data or 'entries' not in har_data['log']:
        return
    
    entries = har_data['log']['entries']
    if not entries:
        return
    
    print("Replaying")
    
    matches = 0
    total = 0
    start_time = None
    
    for i, entry in enumerate(entries):
        if 'request' not in entry or 'response' not in entry:
            continue
            
        request = entry['request']
        recorded_response = entry['response']
        
        # Calculate timing delay
        if start_time is None:
            start_time = entry.get('startedDateTime', '')
        else:
            if 'startedDateTime' in entry and start_time:
                try:
                    from datetime import datetime
                    current_time = datetime.fromisoformat(entry['startedDateTime'].replace('Z', '+00:00'))
                    prev_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    delay = (current_time - prev_time).total_seconds() / speed_multiplier
                    if delay > 0:
                        time.sleep(delay)
                except:
                    pass
        
        # Make the request
        try:
            url = request.get('url', '')
            method = request.get('method', 'GET')
            
            if method == 'GET':
                req = urllib.request.Request(url)
            else:
                # For non-GET requests, we'll still try as GET for simplicity
                req = urllib.request.Request(url)
            
            # Add headers
            headers = request.get('headers', [])
            for header in headers:
                if isinstance(header, dict) and 'name' in header and 'value' in header:
                    req.add_header(header['name'], header['value'])
            
            with urllib.request.urlopen(req, timeout=5) as response:
                live_status = response.getcode()
                live_headers = dict(response.headers)
                live_body = response.read().decode('utf-8', errors='ignore')
        
        except (URLError, HTTPError, Exception):
            # If request fails, consider it a diff
            total += 1
            print(f"Diff: status {recorded_response.get('status', 0)} vs 0")
            continue
        
        # Compare responses
        total += 1
        recorded_status = recorded_response.get('status', 0)
        
        if live_status != recorded_status:
            print(f"Diff: status {recorded_status} vs {live_status}")
        else:
            print("Match")
            matches += 1
    
    # Summary
    if total > 0:
        print(f"Summary: {matches}/{total} matches")

def main():
    # Read input
    file_path = input().strip()
    speed_multiplier = float(input().strip())
    
    # Read and parse HAR file
    har_data = read_har_file(file_path)
    
    # Replay requests
    replay_requests(har_data, speed_multiplier)

if __name__ == "__main__":
    main()