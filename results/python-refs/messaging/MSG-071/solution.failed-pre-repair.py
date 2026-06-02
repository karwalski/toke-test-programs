import sys
import json
import hashlib

def consistent_hash(key, num_partitions):
    """Hash a key and return the partition number."""
    hash_obj = hashlib.md5(key.encode('utf-8'))
    hash_int = int(hash_obj.hexdigest(), 16)
    return hash_int % num_partitions

def main():
    # Read input
    num_partitions = int(input().strip())
    messages_json = input().strip()
    messages = json.loads(messages_json)
    
    # Initialize partitions
    partitions = [[] for _ in range(num_partitions)]
    
    # Assign messages to partitions
    for message in messages:
        partition_key = message["partition_key"]
        text = message["text"]
        partition_num = consistent_hash(partition_key, num_partitions)
        partitions[partition_num].append(f"{text} ({partition_key})")
    
    # Output results
    for i in range(num_partitions):
        if partitions[i]:
            partition_content = ", ".join(partitions[i])
            print(f"partition {i}: [{partition_content}]")
        else:
            print(f"partition {i}: []")

if __name__ == "__main__":
    main()