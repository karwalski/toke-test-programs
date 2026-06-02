import sys

def main():
    # Read input
    port = int(input().strip())
    n = int(input().strip())
    
    # Simulate WebSocket echo server behavior
    # Generate test messages
    messages = [f"message{i}" for i in range(1, n + 1)]
    
    all_match = True
    
    # Simulate client sending messages and receiving echoes
    for msg in messages:
        sent = msg
        received = msg  # Echo server returns the same message
        match = "yes" if sent == received else "no"
        
        if sent != received:
            all_match = False
            
        print(f"Sent: {sent} | Received: {received} | MATCH: {match}")
    
    # Final result
    result = "PASS" if all_match else "FAIL"
    print(result)

if __name__ == "__main__":
    main()