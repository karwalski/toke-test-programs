import json
import sys
from datetime import datetime
from collections import defaultdict

def parse_timestamp(timestamp_str):
    """Parse ISO timestamp and return time part in HH:MM:SS format"""
    dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    return dt.strftime('%H:%M:%S')

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    events = json.loads(input_data)
    
    # Statistics counters
    operation_counts = defaultdict(int)
    key_usage = defaultdict(int)
    total_operations = 0
    successful_operations = 0
    
    # Process events and generate audit log
    print("AUDIT LOG:")
    
    for event in events:
        operation = event['operation']
        key_id = event['key_id']
        msg_id = event['msg_id']
        timestamp = event['timestamp']
        success = event['success']
        
        # Format timestamp
        time_str = parse_timestamp(timestamp)
        
        # Format status
        status = "OK" if success else "FAILED"
        
        # Print audit log entry
        print(f"[{time_str}] {operation} {msg_id} with {key_id}: {status}")
        
        # Update statistics
        operation_counts[operation] += 1
        key_usage[key_id] += 1
        total_operations += 1
        if success:
            successful_operations += 1
    
    print("---")
    
    # Format operations statistics
    operations_parts = []
    for op_type in sorted(operation_counts.keys()):
        operations_parts.append(f"{op_type}={operation_counts[op_type]}")
    print(f"operations: {', '.join(operations_parts)}")
    
    # Calculate and format success rate
    success_rate = (successful_operations / total_operations) * 100 if total_operations > 0 else 0
    print(f"success rate: {success_rate:.1f}% ({successful_operations}/{total_operations})")
    
    # Format key usage statistics
    key_parts = []
    for key_id in sorted(key_usage.keys()):
        key_parts.append(f"{key_id}={key_usage[key_id]}")
    print(f"keys used: {', '.join(key_parts)}")

if __name__ == "__main__":
    main()