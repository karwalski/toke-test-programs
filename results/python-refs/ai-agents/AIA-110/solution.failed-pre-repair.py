import json
import sys

def serialize_agent_state(data):
    """Serialize agent state to a compact format by shortening key names"""
    compact_data = {}
    
    # Map full keys to compact keys
    key_mapping = {
        'user': 'u',
        'context': 'c',
        'turn': 't',
        'metadata': 'm'
    }
    
    for key, value in data.items():
        compact_key = key_mapping.get(key, key)
        compact_data[compact_key] = value
    
    # Serialize to JSON string with minimal spacing
    serialized = json.dumps(compact_data, separators=(',', ':'))
    return serialized

def deserialize_agent_state(serialized_string):
    """Deserialize compact format back to full agent state"""
    compact_data = json.loads(serialized_string)
    
    # Map compact keys back to full keys
    reverse_mapping = {
        'u': 'user',
        'c': 'context', 
        't': 'turn',
        'm': 'metadata'
    }
    
    full_data = {}
    for key, value in compact_data.items():
        full_key = reverse_mapping.get(key, key)
        full_data[full_key] = value
    
    return full_data

def main():
    input_data = json.loads(sys.stdin.read().strip())
    action = input_data['action']
    data = input_data['data']
    
    if action == 'serialise':
        result = serialize_agent_state(data)
        size_bytes = len(result.encode('utf-8'))
        output = {
            'result': result,
            'size_bytes': size_bytes
        }
    elif action == 'deserialise':
        result = deserialize_agent_state(data)
        size_bytes = len(json.dumps(result).encode('utf-8'))
        output = {
            'result': result,
            'size_bytes': size_bytes
        }
    
    print(json.dumps(output, separators=(',', ':')))

if __name__ == '__main__':
    main()