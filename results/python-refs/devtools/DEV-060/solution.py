import socket
import sys

# Read input
line = input().strip()
start_port, end_port = map(int, line.split())

open_ports = []

# Scan ports in the given range
for port in range(start_port, end_port + 1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('localhost', port))
    if result == 0:
        open_ports.append(port)
        print(f"port {port}: OPEN")
    sock.close()

# Print count
print(f"{len(open_ports)} port(s) open")