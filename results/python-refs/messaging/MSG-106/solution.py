import json
import sys
from datetime import datetime

def parse_time(time_str):
    """Parse time string in HH:MM:SS.mmm format to milliseconds"""
    time_obj = datetime.strptime(time_str, "%H:%M:%S.%f")
    return time_obj.hour * 3600000 + time_obj.minute * 60000 + time_obj.second * 1000 + time_obj.microsecond // 1000

def main():
    # Read JSON from stdin
    input_data = sys.stdin.read().strip()
    hops = json.loads(input_data)
    
    # Parse times and calculate latencies
    trace_parts = []
    hop_details = []
    
    for i, hop in enumerate(hops):
        arrived_ms = parse_time(hop["arrived_at"])
        
        # Calculate processing time
        if hop["departed_at"]:
            departed_ms = parse_time(hop["departed_at"])
            processing_time = departed_ms - arrived_ms
        else:
            processing_time = None
        
        # Calculate transit time to next hop
        if i < len(hops) - 1:
            next_arrived_ms = parse_time(hops[i + 1]["arrived_at"])
            if hop["departed_at"]:
                departed_ms = parse_time(hop["departed_at"])
                transit_time = next_arrived_ms - departed_ms
            else:
                transit_time = 0
        else:
            transit_time = None
        
        # Build trace visualization
        if i == 0:
            trace_parts.append(hop["node"])
        
        if transit_time is not None:
            trace_parts.append(f" --[{transit_time}ms]--> ")
            trace_parts.append(hops[i + 1]["node"])
        
        # Build hop details
        if processing_time is not None:
            hop_details.append(f"hop {i + 1}: {hop['node']} ({processing_time}ms processing, {hop['action']})")
        else:
            hop_details.append(f"hop {i + 1}: {hop['node']} ({hop['action']})")
    
    # Calculate total end-to-end time
    start_time = parse_time(hops[0]["arrived_at"])
    end_time = parse_time(hops[-1]["arrived_at"])
    total_time = end_time - start_time
    
    # Output results
    print("".join(trace_parts))
    for detail in hop_details:
        print(detail)
    print(f"total: {total_time}ms end-to-end")

if __name__ == "__main__":
    main()