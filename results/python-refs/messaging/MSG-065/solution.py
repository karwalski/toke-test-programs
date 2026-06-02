import json
import sys

def solve():
    max_retry_count = int(input().strip())
    attempts_json = input().strip()
    attempts = json.loads(attempts_json)
    
    # Track message states
    messages = {}
    
    for attempt in attempts:
        msg_id = attempt["msg_id"]
        attempt_num = attempt["attempt"]
        success = attempt["success"]
        time = attempt["time"]
        
        if msg_id not in messages:
            messages[msg_id] = {
                "failures": 0,
                "delivered": False,
                "last_error_time": None,
                "attempts": 0
            }
        
        messages[msg_id]["attempts"] = max(messages[msg_id]["attempts"], attempt_num)
        
        if success:
            messages[msg_id]["delivered"] = True
        else:
            messages[msg_id]["failures"] += 1
            messages[msg_id]["last_error_time"] = time
    
    # Separate DLQ and delivered messages
    dlq_messages = []
    delivered_messages = []
    
    for msg_id, info in messages.items():
        if info["delivered"]:
            delivered_messages.append((msg_id, info["attempts"]))
        elif info["failures"] >= max_retry_count:
            dlq_messages.append((msg_id, info["failures"], info["last_error_time"]))
    
    # Output DLQ messages
    print("DLQ:")
    for msg_id, failures, last_time in dlq_messages:
        print(f"  {msg_id} ({failures} failures, last: {last_time})")
    
    # Output delivered messages
    print("DELIVERED:")
    for msg_id, attempts in delivered_messages:
        print(f"  {msg_id} ({attempts} attempt{'s' if attempts != 1 else ''})")

solve()