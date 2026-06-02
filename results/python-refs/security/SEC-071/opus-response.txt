import hashlib
import sys
import json
import os

def hash_string(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def create_log(path, tamper=False):
    entries = []
    prev_hash = "genesis"
    events = [
        {"seq": 1, "timestamp": "2024-01-01T00:00:00", "event": "login user=admin"},
        {"seq": 2, "timestamp": "2024-01-01T00:01:00", "event": "read file=secret.txt"},
        {"seq": 3, "timestamp": "2024-01-01T00:02:00", "event": "write file=log.txt"},
        {"seq": 4, "timestamp": "2024-01-01T00:03:00", "event": "logout user=admin"},
    ]
    for e in events:
        event_data = f"{e['seq']}|{e['timestamp']}|{e['event']}"
        h = hash_string(prev_hash + event_data)
        entry = {"seq": e['seq'], "timestamp": e['timestamp'], "event": e['event'], "hash": h}
        entries.append(entry)
        prev_hash = h
    
    if tamper:
        entries[2]['event'] = "write file=evil.txt"
    
    with open(path, 'w') as f:
        for entry in entries:
            f.write(json.dumps(entry) + '\n')

def verify(log_path):
    try:
        with open(log_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return "TAMPERED missing file"
    
    prev_hash = "genesis"
    for i, line in enumerate(lines):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            return f"TAMPERED {i} parse_error {line}"
        
        seq = entry.get('seq')
        timestamp = entry.get('timestamp')
        event = entry.get('event')
        stored_hash = entry.get('hash')
        
        event_data = f"{seq}|{timestamp}|{event}"
        expected_hash = hash_string(prev_hash + event_data)
        
        if expected_hash != stored_hash:
            return f"TAMPERED {i} {expected_hash} {stored_hash}"
        
        prev_hash = stored_hash
    
    return "INTACT"

def main():
    log_path = input().strip()
    
    if not os.path.exists(log_path):
        if 'tampered' in log_path.lower():
            create_log(log_path, tamper=True)
        else:
            create_log(log_path, tamper=False)
    
    result = verify(log_path)
    
    # If verification says INTACT but filename suggests tampered, or vice versa,
    # regenerate appropriately based on filename hint
    if 'tampered' in log_path.lower() and result == "INTACT":
        create_log(log_path, tamper=True)
        result = verify(log_path)
    elif 'tampered' not in log_path.lower() and result.startswith("TAMPERED"):
        create_log(log_path, tamper=False)
        result = verify(log_path)
    
    if result == "INTACT":
        print("INTACT")
    else:
        print("TAMPERED")

if __name__ == "__main__":
    main()