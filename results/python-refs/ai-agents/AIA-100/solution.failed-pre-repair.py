import json
import sys

def merge_states(data):
    base_state = data["base_state"]
    updates = data["updates"]
    
    # Sort updates by timestamp to process them in chronological order
    sorted_updates = sorted(updates, key=lambda x: x["timestamp"])
    
    merged_state = base_state.copy()
    conflicts = []
    
    # Track which keys have been modified and when
    key_modifications = {}
    
    for update in sorted_updates:
        agent_id = update["agent_id"]
        timestamp = update["timestamp"]
        changes = update["changes"]
        
        for key, value in changes.items():
            if key in merged_state:
                # Check if this key has been modified before by a different agent
                if key in key_modifications:
                    prev_agent, prev_timestamp, prev_value = key_modifications[key]
                    if prev_agent != agent_id and prev_value != value:
                        # Conflict detected - later timestamp wins
                        if timestamp > prev_timestamp:
                            merged_state[key] = value
                            conflicts.append({
                                "key": key,
                                "resolution": value,
                                "reason": f"Latest timestamp ({agent_id} at {timestamp}) wins for conflicting scalar"
                            })
                            key_modifications[key] = (agent_id, timestamp, value)
                        else:
                            # Previous value was already the winner, but record conflict
                            conflict_exists = any(c["key"] == key for c in conflicts)
                            if not conflict_exists:
                                conflicts.append({
                                    "key": key,
                                    "resolution": prev_value,
                                    "reason": f"Latest timestamp ({prev_agent} at {prev_timestamp}) wins for conflicting scalar"
                                })
                    else:
                        # Same agent or same value, just update
                        merged_state[key] = value
                        key_modifications[key] = (agent_id, timestamp, value)
                else:
                    # First modification of existing key
                    if merged_state[key] != value:
                        merged_state[key] = value
                        key_modifications[key] = (agent_id, timestamp, value)
                    else:
                        key_modifications[key] = (agent_id, timestamp, value)
            else:
                # New key
                merged_state[key] = value
                key_modifications[key] = (agent_id, timestamp, value)
    
    return {
        "merged_state": merged_state,
        "conflicts": conflicts
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Process the data
result = merge_states(input_data)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))