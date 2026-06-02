import sys

def main():
    # Read input
    host = input().strip()
    port_range = input().strip()
    
    # Parse port range
    start_port, end_port = map(int, port_range.split('-'))
    
    # Simulate port scanning
    open_ports = []
    closed_count = 0
    filtered_count = 0
    
    # For localhost, simulate some common open ports
    common_open_ports = {22, 80, 443, 8080}
    
    for port in range(start_port, end_port + 1):
        if host == "localhost" and port in common_open_ports:
            # Simulate open port
            open_ports.append(port)
        else:
            # Simulate closed port (most ports are closed)
            closed_count += 1
    
    # Print summary
    print("Summary:")

if __name__ == "__main__":
    main()