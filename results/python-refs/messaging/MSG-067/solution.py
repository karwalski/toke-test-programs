import json
import sys
from datetime import datetime
from collections import Counter

def parse_duration(start_time, end_time):
    start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
    end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
    duration_seconds = int((end - start).total_seconds())
    
    if duration_seconds < 60:
        return f"{duration_seconds}s"
    else:
        minutes = duration_seconds // 60
        return f"{minutes}m"

def generate_conversation_summary(messages):
    if not messages:
        return ""
    
    # Message count
    message_count = len(messages)
    
    # Active participants
    participant_counts = Counter(msg['sender'] for msg in messages)
    total_participants = len(participant_counts)
    
    # Time span
    times = [msg['time'] for msg in messages]
    first_time = min(times)
    last_time = max(times)
    duration = parse_duration(first_time, last_time)
    
    # Message type distribution
    type_counts = Counter(msg['type'] for msg in messages)
    
    # Format output
    result = []
    result.append(f"messages: {message_count}")
    
    # Format participants
    participant_details = ", ".join(f"{name}: {count}" for name, count in sorted(participant_counts.items()))
    result.append(f"participants: {total_participants} ({participant_details})")
    
    result.append(f"duration: {duration}")
    
    # Format types
    type_details = ", ".join(f"{msg_type}={count}" for msg_type, count in sorted(type_counts.items()))
    result.append(f"types: {type_details}")
    
    result.append(f"first: {first_time}")
    result.append(f"last: {last_time}")
    
    return "\n".join(result)

# Read input from stdin
input_data = sys.stdin.read().strip()
messages = json.loads(input_data)

# Generate and print summary
summary = generate_conversation_summary(messages)
print(summary)