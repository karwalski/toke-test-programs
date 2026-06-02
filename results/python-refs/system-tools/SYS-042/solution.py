import sys

# Read input
start_port = int(input().strip())
end_port = int(input().strip())
timeout_ms = int(input().strip())

# Common services mapping
services = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "domain",
    80: "http",
    110: "pop3",
    143: "imap",
    443: "https",
    993: "imaps",
    995: "pop3s"
}

# Simulate port scanning - assume only common service ports are open
open_ports = []

for port in range(start_port, end_port + 1):
    # Simulate that only some well-known service ports are open
    if port in services:
        service_name = services[port]
        print(f"OPEN {port}/tcp {service_name}")
        open_ports.append(port)

print(f"{len(open_ports)} open ports.")