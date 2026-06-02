import socket
import threading
import time
import sys
from concurrent.futures import ThreadPoolExecutor

def get_service_guess(port):
    services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        993: "IMAPS",
        995: "POP3S"
    }
    return services.get(port, "Unknown")

def check_port(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return port, "OPEN"
        else:
            return port, "CLOSED"
    except:
        return port, "FILTERED"

def main():
    # Read input
    host = input().strip()
    port_range = input().strip()
    concurrency = int(input().strip())
    
    # Parse port range
    start_port, end_port = map(int, port_range.split('-'))
    ports = list(range(start_port, end_port + 1))
    
    open_ports = []
    start_time = time.time()
    
    # Scan ports concurrently
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(check_port, host, port) for port in ports]
        for future in futures:
            port, status = future.result()
            if status == "OPEN":
                open_ports.append(port)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print("Summary:")

if __name__ == "__main__":
    main()