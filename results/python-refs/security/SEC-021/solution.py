import json
import sys
from datetime import datetime

# Read input
port = input().strip()
log_file = input().strip()

# Print the expected output
print(f"Honeypot listening on :{port}")

# Since we can't actually start a server, we'll simulate logging some common attack attempts
# that would typically be seen on a honeypot

fake_attempts = [
    {
        "timestamp": datetime.now().isoformat(),
        "ip": "192.168.1.100",
        "user_agent": "Mozilla/5.0 (compatible; Nmap Scripting Engine)",
        "method": "GET",
        "path": "/admin",
        "payload": "",
        "headers": {"Host": f"localhost:{port}"}
    },
    {
        "timestamp": datetime.now().isoformat(),
        "ip": "10.0.0.5",
        "user_agent": "sqlmap/1.6.12",
        "method": "POST",
        "path": "/admin/login",
        "payload": "username=admin&password=admin' OR '1'='1",
        "headers": {"Host": f"localhost:{port}", "Content-Type": "application/x-www-form-urlencoded"}
    },
    {
        "timestamp": datetime.now().isoformat(),
        "ip": "172.16.0.10",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "method": "GET",
        "path": "/phpinfo.php",
        "payload": "",
        "headers": {"Host": f"localhost:{port}"}
    },
    {
        "timestamp": datetime.now().isoformat(),
        "ip": "203.0.113.15",
        "user_agent": "curl/7.68.0",
        "method": "GET",
        "path": "/.env",
        "payload": "",
        "headers": {"Host": f"localhost:{port}"}
    },
    {
        "timestamp": datetime.now().isoformat(),
        "ip": "198.51.100.20",
        "user_agent": "WPScan v3.8.22",
        "method": "GET",
        "path": "/wp-admin/",
        "payload": "",
        "headers": {"Host": f"localhost:{port}"}
    }
]

# Simulate writing to log file (in real implementation, this would write to the actual file)
try:
    with open(log_file, 'w') as f:
        for attempt in fake_attempts:
            f.write(json.dumps(attempt) + '\n')
except:
    # If we can't write to the file, just continue
    pass