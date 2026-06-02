import hashlib
import sys

def hash_string(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def main():
    log_path = input().strip()
    
    try:
        with open(log_path, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print("TAMPERED")
        return
    
    if not lines:
        print("INTACT")
        return
    
    # First entry should have no previous hash dependency
    # Assume format: "index:timestamp:data:hash"
    # Hash is computed from "index:timestamp:data:prev_hash"
    
    prev_hash = ""
    
    for i, line in enumerate(lines):
        parts = line.split(':')
        if len(parts) < 4:
            print(f"TAMPERED {i} {''} {''}")
            return
        
        index = parts[0]
        timestamp = parts[1]
        data = parts[2]
        stored_hash = parts[3]
        
        # Construct the string to hash: index:timestamp:data:prev_hash
        hash_input = f"{index}:{timestamp}:{data}:{prev_hash}"
        expected_hash = hash_string(hash_input)
        
        if expected_hash != stored_hash:
            print(f"TAMPERED {i} {expected_hash} {stored_hash}")
            return
        
        prev_hash = stored_hash
    
    print("INTACT")

if __name__ == "__main__":
    main()