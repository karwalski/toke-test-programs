import json
import sys

def process_delivery_events():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    events = json.loads(input_data)
    
    # Track message delivery state
    # Key: (msg_id, txn_id), Value: {'delivered': bool, 'first_attempt': int, 'duplicates': []}
    message_state = {}
    
    # Process each event
    for event in events:
        msg_id = event['msg_id']
        txn_id = event['txn_id']
        attempt = event['attempt']
        consumer = event['consumer']
        
        key = (msg_id, txn_id)
        
        if key not in message_state:
            # First time seeing this message/transaction combination
            message_state[key] = {
                'delivered': True,
                'first_attempt': attempt,
                'duplicates': []
            }
        else:
            # Duplicate delivery attempt - suppress it
            message_state[key]['duplicates'].append(attempt)
    
    # Generate output
    total_messages = len(message_state)
    total_events = len(events)
    total_duplicates = sum(len(state['duplicates']) for state in message_state.values())
    
    # Sort messages by their first appearance in the input for consistent output
    msg_order = {}
    for i, event in enumerate(events):
        key = (event['msg_id'], event['txn_id'])
        if key not in msg_order:
            msg_order[key] = i
    
    sorted_messages = sorted(message_state.keys(), key=lambda x: msg_order[x])
    
    # Output per-message results
    for msg_id, txn_id in sorted_messages:
        state = message_state[(msg_id, txn_id)]
        if state['duplicates']:
            duplicates_str = ", duplicate suppressed at attempt " + ", ".join(map(str, sorted(state['duplicates'])))
            print(f"{msg_id}: delivered-once (attempt {state['first_attempt']}{duplicates_str})")
        else:
            print(f"{msg_id}: delivered-once (attempt {state['first_attempt']})")
    
    # Output summary
    print("---")
    print(f"total: {total_messages} messages, {total_events} events, {total_duplicates} duplicate suppressed")

if __name__ == "__main__":
    process_delivery_events()