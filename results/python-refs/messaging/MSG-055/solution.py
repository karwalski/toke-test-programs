import json
import sys
from datetime import datetime, timedelta

def time_to_seconds(time_str):
    """Convert time string to seconds since midnight"""
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def calculate_similarity(text1, text2):
    """Calculate similarity between two texts using character-level comparison"""
    text1 = text1.lower()
    text2 = text2.lower()
    
    if len(text1) == 0 and len(text2) == 0:
        return 1.0
    if len(text1) == 0 or len(text2) == 0:
        return 0.0
    
    # Simple character-based similarity
    max_len = max(len(text1), len(text2))
    min_len = min(len(text1), len(text2))
    
    # Count matching characters at same positions
    matches = 0
    for i in range(min_len):
        if text1[i] == text2[i]:
            matches += 1
    
    # Add penalty for length difference
    length_penalty = abs(len(text1) - len(text2)) / max_len
    similarity = (matches / max_len) * (1 - length_penalty * 0.5)
    
    # Alternative approach: use set intersection
    set1 = set(text1)
    set2 = set(text2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    if union == 0:
        jaccard = 1.0
    else:
        jaccard = intersection / union
    
    # Combine both approaches
    return max(similarity, jaccard)

# Read input
similarity_threshold = float(input().strip())
time_window = int(input().strip())
max_similar_messages = int(input().strip())
messages_json = input().strip()

messages = json.loads(messages_json)

# Convert times to seconds and group by sender
sender_messages = {}
for msg in messages:
    sender = msg['sender']
    if sender not in sender_messages:
        sender_messages[sender] = []
    
    time_seconds = time_to_seconds(msg['time'])
    sender_messages[sender].append({
        'text': msg['text'],
        'time': time_seconds,
        'original_time': msg['time']
    })

# Sort messages by time for each sender
for sender in sender_messages:
    sender_messages[sender].sort(key=lambda x: x['time'])

# Check for flooding
for sender, msgs in sender_messages.items():
    for i in range(len(msgs)):
        similar_messages = [msgs[i]]
        start_time = msgs[i]['time']
        
        # Check messages within time window
        for j in range(i + 1, len(msgs)):
            if msgs[j]['time'] - start_time > time_window:
                break
            
            # Check if this message is similar to any in the current group
            for similar_msg in similar_messages:
                if calculate_similarity(msgs[j]['text'], similar_msg['text']) >= similarity_threshold:
                    similar_messages.append(msgs[j])
                    break
        
        # Check if we found flooding
        if len(similar_messages) >= max_similar_messages:
            count = len(similar_messages)
            time_span = similar_messages[-1]['time'] - similar_messages[0]['time']
            print(f"FLOOD: {sender} sent {count} similar messages in {time_span}s (threshold: {max_similar_messages} in {time_window}s)")
            break