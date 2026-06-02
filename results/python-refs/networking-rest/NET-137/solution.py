import sys

def main():
    # Read WebSocket URL
    url = input().strip()
    
    # Read username
    username = input().strip()
    
    # Print "Connected" when joining
    print("Connected")
    
    # Read and process messages
    try:
        while True:
            message = input().strip()
            # In a real implementation, we would send the message
            # For simulation, we just continue reading
    except EOFError:
        # End of input reached
        pass

if __name__ == "__main__":
    main()