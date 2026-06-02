import sys
import re

# Apache Combined Log Format regex pattern
pattern = r'^(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) [^"]*" (\d+) (\S+)'

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    match = re.match(pattern, line)
    if match:
        ip = match.group(1)
        timestamp = match.group(2)
        method = match.group(3)
        path = match.group(4)
        status = match.group(5)
        bytes_sent = match.group(6)
        
        print(f"{ip}\t{timestamp}\t{method}\t{path}\t{status}\t{bytes_sent}")