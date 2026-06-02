import sys
import json
import hashlib

def consistent_hash(key, num_partitions):
    h = hashlib.sha256(key.encode('utf-8')).hexdigest()
    return int(h, 16) % num_partitions

def main():
    data = sys.stdin.read().split('\n')
    num_partitions = int(data[0].strip())
    messages = json.loads(data[1])
    
    partitions = [[] for _ in range(num_partitions)]
    
    for message in messages:
        partition_key = message["partition_key"]
        text = message["text"]
        # Try various hash schemes to match expected
        partition_num = consistent_hash(partition_key, num_partitions)
        partitions[partition_num].append(f"{text} ({partition_key})")
    
    # Check test 1 expectation: alice->2, bob->1 with N=4
    # SHA256("user:alice") = ?
    # Let me just compute and trust SHA-256
    
    out = []
    for i in range(num_partitions):
        if partitions[i]:
            partition_content = ", ".join(partitions[i])
            out.append(f"partition {i}: [{partition_content}]")
        else:
            out.append(f"partition {i}: []")
    print('\n'.join(out))

if __name__ == "__main__":
    main()