import sys
import ipaddress

for line in sys.stdin:
    line = line.strip()
    if line:
        network = ipaddress.IPv4Network(line, strict=False)
        for ip in network:
            print(ip)