import sys

storage = {}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    command = parts[0]
    
    if command == "SSTORE":
        key = parts[1]
        value = parts[2]
        storage[key] = value
    elif command == "SLOAD":
        key = parts[1]
        value = storage.get(key, "0")
        print(value)