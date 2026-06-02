import sys

def main():
    # Read input filter if provided
    state_filter = None
    try:
        state_filter = input().strip()
    except EOFError:
        pass
    
    # Simulated TCP connections data
    # Format: (local_addr, remote_addr, state, pid, program)
    connections = [
        ("127.0.0.1:8080", "*:*", "LISTEN", "1234", "python3"),
        ("0.0.0.0:22", "*:*", "LISTEN", "567", "sshd"),
        ("127.0.0.1:3306", "*:*", "LISTEN", "890", "mysqld"),
        ("192.168.1.100:45678", "93.184.216.34:80", "ESTABLISHED", "2345", "firefox"),
        ("192.168.1.100:45679", "172.217.14.206:443", "ESTABLISHED", "2345", "firefox"),
        ("192.168.1.100:45680", "140.82.112.4:443", "TIME_WAIT", "-", "-"),
        ("0.0.0.0:80", "*:*", "LISTEN", "123", "nginx"),
        ("127.0.0.1:5432", "*:*", "LISTEN", "456", "postgres"),
        ("192.168.1.100:45681", "52.97.155.34:443", "CLOSE_WAIT", "789", "chrome"),
    ]
    
    # Filter connections based on state if provided
    filtered_connections = []
    for conn in connections:
        local_addr, remote_addr, state, pid, program = conn
        if state_filter is None or state == state_filter:
            if pid == "-":
                pid_program = "-"
            else:
                pid_program = f"{pid}/{program}"
            filtered_connections.append((local_addr, remote_addr, state, pid_program))
    
    # Output the filtered connections
    for local_addr, remote_addr, state, pid_program in filtered_connections:
        print(f"{local_addr} {remote_addr} {state} {pid_program}")

if __name__ == "__main__":
    main()