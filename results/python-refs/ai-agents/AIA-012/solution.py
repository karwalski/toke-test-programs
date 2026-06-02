import json
import sys

def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)
    
    call = input_data['call']
    cache = input_data['cache']
    now_ms = input_data['now_ms']
    ttl_ms = input_data['ttl_ms']
    
    # Check each cache entry
    for entry in cache:
        # Check if tool matches
        if entry['tool'] != call['tool']:
            continue
            
        # Check if arguments match exactly
        if entry['arguments'] != call['arguments']:
            continue
            
        # Check if cache entry is still valid (within TTL)
        cached_at_ms = entry['cached_at_ms']
        if now_ms - cached_at_ms > ttl_ms:
            continue
            
        # Cache hit - return the cached result
        result = {
            "cache_hit": True,
            "result": entry['result']
        }
        print(json.dumps(result, separators=(',', ':')))
        return
    
    # No cache hit found
    result = {
        "cache_hit": False,
        "result": None
    }
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()