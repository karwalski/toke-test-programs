import json
import sys

def process_delivery_guarantees():
    lines = sys.stdin.read().strip().split('\n')
    guarantee_level = lines[0]
    events = json.loads(lines[1])
    
    # Track message states and traces
    messages = {}
    
    for event in events:
        msg_id = event['msg_id']
        event_type = event['event']
        
        if msg_id not in messages:
            messages[msg_id] = {
                'trace': [],
                'status': 'PENDING',
                'sent_count': 0,
                'acked': False
            }
        
        msg = messages[msg_id]
        msg['trace'].append(event_type)
        
        if event_type == 'send':
            msg['sent_count'] += 1
        elif event_type == 'ack':
            msg['acked'] = True
            if guarantee_level == 'exactly-once':
                msg['status'] = 'DELIVERED'
            elif guarantee_level == 'at-least-once':
                msg['status'] = 'DELIVERED'
            elif guarantee_level == 'at-most-once':
                msg['status'] = 'DELIVERED'
        elif event_type == 'timeout':
            if guarantee_level == 'at-most-once':
                msg['status'] = 'LOST'
            elif guarantee_level == 'at-least-once':
                msg['status'] = 'PENDING'  # Will retry
            elif guarantee_level == 'exactly-once':
                msg['status'] = 'PENDING'  # Will retry
        elif event_type == 'retry':
            if guarantee_level == 'at-most-once':
                # No retries in at-most-once
                pass
            else:
                msg['status'] = 'PENDING'
    
    # Final status determination
    delivered_count = 0
    lost_count = 0
    
    for msg_id, msg in messages.items():
        trace_str = ' -> '.join(msg['trace'])
        
        if msg['acked']:
            final_status = 'DELIVERED'
            delivered_count += 1
        else:
            if guarantee_level == 'at-most-once':
                final_status = 'LOST'
                lost_count += 1
                reason = f"({guarantee_level}: no retry)"
            elif guarantee_level == 'at-least-once':
                if 'timeout' in msg['trace'] and 'retry' not in msg['trace']:
                    final_status = 'PENDING'
                    reason = f"({guarantee_level}: will retry)"
                else:
                    final_status = 'LOST'
                    lost_count += 1
                    reason = f"({guarantee_level}: retry failed)"
            elif guarantee_level == 'exactly-once':
                if 'timeout' in msg['trace'] and 'retry' not in msg['trace']:
                    final_status = 'PENDING'
                    reason = f"({guarantee_level}: will retry)"
                else:
                    final_status = 'LOST'
                    lost_count += 1
                    reason = f"({guarantee_level}: retry failed)"
        
        if final_status == 'DELIVERED':
            if guarantee_level == 'exactly-once' and msg['sent_count'] > 1:
                reason = f"({guarantee_level}: deduplicated)"
            else:
                reason = ""
        elif final_status == 'LOST':
            if guarantee_level == 'at-most-once':
                reason = f"({guarantee_level}: no retry)"
            else:
                reason = f"({guarantee_level}: delivery failed)"
        
        if reason:
            print(f"{msg_id}: {trace_str} -> {final_status} {reason}")
        else:
            print(f"{msg_id}: {trace_str} -> {final_status}")
    
    print(f"delivered: {delivered_count}, lost: {lost_count}")

if __name__ == "__main__":
    process_delivery_guarantees()