import json
import sys
from collections import defaultdict
import re
from datetime import datetime

def parse_timestamp(timestamp_str):
    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

def detect_sequential_enumeration(requests):
    """Detect sequential ID enumeration patterns"""
    patterns = []
    
    # Group by IP and look for sequential patterns
    ip_requests = defaultdict(list)
    for req in requests:
        ip_requests[req['ip']].append(req)
    
    for ip, ip_reqs in ip_requests.items():
        # Look for sequential ID patterns in paths
        id_requests = []
        for req in ip_reqs:
            # Extract numeric IDs from paths like /users/123, /api/v1/posts/456
            match = re.search(r'/(\d+)(?:/|$)', req['path'])
            if match:
                id_requests.append((int(match.group(1)), req))
        
        if len(id_requests) >= 3:
            # Sort by timestamp
            id_requests.sort(key=lambda x: x[1]['timestamp'])
            
            # Check for sequential IDs
            sequential_count = 1
            for i in range(1, len(id_requests)):
                if id_requests[i][0] == id_requests[i-1][0] + 1:
                    sequential_count += 1
                else:
                    if sequential_count >= 3:
                        break
                    sequential_count = 1
            
            if sequential_count >= 3:
                patterns.append({
                    "type": "scraping",
                    "ip": ip,
                    "evidence": f"Sequential ID enumeration detected ({sequential_count} consecutive IDs)",
                    "severity": "high" if sequential_count >= 10 else "medium",
                    "recommendation": "Block IP and implement rate limiting on ID-based endpoints"
                })
    
    return patterns

def detect_account_takeover(requests):
    """Detect account takeover patterns"""
    patterns = []
    
    ip_requests = defaultdict(list)
    for req in requests:
        ip_requests[req['ip']].append(req)
    
    for ip, ip_reqs in ip_requests.items():
        # Look for login attempts and user access patterns
        login_attempts = []
        user_accesses = set()
        
        for req in ip_reqs:
            if '/login' in req['path'] or '/auth' in req['path']:
                login_attempts.append(req)
            if req['user_id'] != 'anon':
                user_accesses.add(req['user_id'])
        
        # Multiple failed logins or access to multiple user accounts
        failed_logins = sum(1 for req in login_attempts if req['status'] >= 400)
        
        if failed_logins >= 5:
            patterns.append({
                "type": "account_takeover",
                "ip": ip,
                "evidence": f"Multiple failed login attempts ({failed_logins} failures)",
                "severity": "high",
                "recommendation": "Implement account lockout and CAPTCHA"
            })
        elif len(user_accesses) >= 5:
            patterns.append({
                "type": "account_takeover",
                "ip": ip,
                "evidence": f"Access to multiple user accounts ({len(user_accesses)} accounts)",
                "severity": "medium",
                "recommendation": "Monitor for unauthorized access patterns"
            })
    
    return patterns

def detect_volumetric_attacks(requests):
    """Detect volumetric attack patterns"""
    patterns = []
    
    ip_requests = defaultdict(list)
    for req in requests:
        ip_requests[req['ip']].append(req)
    
    for ip, ip_reqs in ip_requests.items():
        # High request volume in short time
        if len(ip_reqs) >= 50:
            patterns.append({
                "type": "volumetric_attack",
                "ip": ip,
                "evidence": f"High request volume ({len(ip_reqs)} requests)",
                "severity": "high" if len(ip_reqs) >= 100 else "medium",
                "recommendation": "Implement rate limiting and DDoS protection"
            })
    
    return patterns

def detect_token_harvesting(requests):
    """Detect token harvesting patterns"""
    patterns = []
    
    ip_requests = defaultdict(list)
    for req in requests:
        ip_requests[req['ip']].append(req)
    
    for ip, ip_reqs in ip_requests.items():
        # Look for token/auth related endpoints
        token_requests = []
        for req in ip_reqs:
            if any(keyword in req['path'].lower() for keyword in ['/token', '/auth', '/oauth', '/api/key']):
                token_requests.append(req)
        
        if len(token_requests) >= 10:
            patterns.append({
                "type": "token_harvesting",
                "ip": ip,
                "evidence": f"Multiple token/auth endpoint accesses ({len(token_requests)} requests)",
                "severity": "high",
                "recommendation": "Implement token rotation and monitoring"
            })
    
    return patterns

def main():
    requests = []
    
    # Read JSON log entries from stdin
    for line in sys.stdin:
        line = line.strip()
        if line:
            try:
                req = json.loads(line)
                requests.append(req)
            except json.JSONDecodeError:
                continue
    
    # Detect abuse patterns
    abuse_patterns = []
    
    abuse_patterns.extend(detect_sequential_enumeration(requests))
    abuse_patterns.extend(detect_account_takeover(requests))
    abuse_patterns.extend(detect_volumetric_attacks(requests))
    abuse_patterns.extend(detect_token_harvesting(requests))
    
    # Output result
    print("abuse_patterns")

if __name__ == "__main__":
    main()