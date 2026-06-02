import json
import sys

def merge_states(data):
    base_state = data["base_state"]
    updates = data["updates"]
    
    sorted_updates = sorted(updates, key=lambda x: x["timestamp"])
    
    merged_state = dict(base_state)
    conflicts = []
    key_modifications = {}
    
    for update in sorted_updates:
        agent_id = update["agent_id"]
        timestamp = update["timestamp"]
        changes = update["changes"]
        
        for key, value in changes.items():
            if isinstance(value, list) and key in merged_state and isinstance(merged_state[key], list):
                if key in key_modifications:
                    prev_agent, prev_timestamp, _ = key_modifications[key]
                    if prev_agent != agent_id and prev_timestamp == timestamp:
                        combined = list(merged_state[key])
                        for item in value:
                            if item not in combined:
                                combined.append(item)
                        merged_state[key] = combined
                        if not any(c["key"] == key for c in conflicts):
                            conflicts.append({
                                "key": key,
                                "resolution": "merged arrays",
                                "reason": "Concurrent array updates combined"
                            })
                        key_modifications[key] = (agent_id, timestamp, combined)
                        continue
                combined = list(merged_state[key])
                for item in value:
                    if item not in combined:
                        combined.append(item)
                merged_state[key] = combined
                key_modifications[key] = (agent_id, timestamp, combined)
            elif key in merged_state:
                if key in key_modifications:
                    prev_agent, prev_timestamp, prev_value = key_modifications[key]
                    if prev_agent != agent_id and prev_value != value:
                        if timestamp > prev_timestamp:
                            merged_state[key] = value
                            if base_state.get(key) != prev_value:
                                conflicts.append({
                                    "key": key,
                                    "resolution": value,
                                    "reason": f"Latest timestamp ({agent_id} at {timestamp}) wins for conflicting scalar"
                                })
                            key_modifications[key] = (agent_id, timestamp, value)
                        else:
                            if not any(c["key"] == key for c in conflicts):
                                if base_state.get(key) != prev_value:
                                    conflicts.append({
                                        "key": key,
                                        "resolution": prev_value,
                                        "reason": f"Latest timestamp ({prev_agent} at {prev_timestamp}) wins for conflicting scalar"
                                    })
                    else:
                        merged_state[key] = value
                        key_modifications[key] = (agent_id, timestamp, value)
                else:
                    if merged_state[key] != value:
                        merged_state[key] = value
                    key_modifications[key] = (agent_id, timestamp, value)
            else:
                merged_state[key] = value
                key_modifications[key] = (agent_id, timestamp, value)
    
    return {
        "merged_state": merged_state,
        "conflicts": conflicts
    }

input_data = json.loads(sys.stdin.read().strip())
result = merge_states(input_data)
print(json.dumps(result, separators=(',', ':')))