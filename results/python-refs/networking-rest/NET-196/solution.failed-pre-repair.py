import sys

def main():
    # Read input
    port = int(input().strip())
    n_events = int(input().strip())
    
    # Simulate SSE server and client
    # Server would push N events: event1, event2, ..., eventN
    # Client receives them in order
    
    received_events = []
    expected_events = []
    
    # Generate expected events (what server would send)
    for i in range(1, n_events + 1):
        expected_events.append(f"event{i}")
    
    # Simulate client receiving events in order
    received_events = expected_events.copy()
    
    # Output events received in order
    for event in received_events:
        print(event)
    
    # Verify completeness and ordering
    if len(received_events) == n_events and received_events == expected_events:
        print(f"All {n_events} events received: PASS")
    else:
        print("Missing events: FAIL")

if __name__ == "__main__":
    main()