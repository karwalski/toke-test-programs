import json
import sys
from datetime import datetime, timezone
import re

def get_country_from_ip(ip):
    # Simple heuristic based on IP ranges (very basic approximation)
    parts = ip.split('.')
    if len(parts) != 4:
        return "Unknown"
    
    try:
        first_octet = int(parts[0])
        # Very basic country detection based on first octet
        if first_octet in range(1, 24):
            return "US"
        elif first_octet in range(24, 48):
            return "EU"
        elif first_octet in range(48, 72):
            return "Asia"
        elif first_octet in range(72, 96):
            return "US"
        elif first_octet in range(96, 120):
            return "Asia"
        elif first_octet in range(120, 144):
            return "Asia"
        elif first_octet in range(144, 168):
            return "US"
        elif first_octet in range(168, 192):
            return "EU"
        elif first_octet in range(192, 216):
            return "US"
        elif first_octet in range(216, 240):
            return "US"
        else:
            return "Other"
    except:
        return "Unknown"

def is_suspicious_user_agent(user_agent):
    suspicious_patterns = [
        r'bot',
        r'crawler',
        r'spider',
        r'scraper',
        r'python',
        r'curl',
        r'wget',
        r'^$',  # empty string
    ]
    
    user_agent_lower = user_agent.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, user_agent_lower):
            return True
    
    # Check for very short user agents
    if len(user_agent) < 10:
        return True
    
    return False

def audit_sessions(sessions):
    issues = []
    now = datetime.now(timezone.utc)
    user_sessions = {}
    
    for session in sessions:
        session_id = session['sessionId']
        user_id = session['userId']
        created_at = datetime.fromisoformat(session['createdAt'].replace('Z', '+00:00'))
        last_active_at = datetime.fromisoformat(session['lastActiveAt'].replace('Z', '+00:00'))
        ip = session['ip']
        user_agent = session['userAgent']
        expires_at = session.get('expiresAt')
        
        # Check for sessions without expiry
        if expires_at is None:
            issues.append({
                "sessionId": session_id,
                "issue_type": "no_expiry",
                "severity": "high",
                "recommendation": "Set session expiry time"
            })
        
        # Check for sessions older than 24h
        time_since_created = now - created_at
        if time_since_created.total_seconds() > 24 * 3600:
            issues.append({
                "sessionId": session_id,
                "issue_type": "old_session",
                "severity": "medium",
                "recommendation": "Terminate old sessions"
            })
        
        # Check for suspicious user agents
        if is_suspicious_user_agent(user_agent):
            issues.append({
                "sessionId": session_id,
                "issue_type": "suspicious_user_agent",
                "severity": "medium",
                "recommendation": "Verify legitimate user"
            })
        
        # Group sessions by user for concurrent session analysis
        if user_id not in user_sessions:
            user_sessions[user_id] = []
        user_sessions[user_id].append({
            'sessionId': session_id,
            'ip': ip,
            'country': get_country_from_ip(ip)
        })
    
    # Check for concurrent sessions from different countries
    for user_id, sessions_list in user_sessions.items():
        if len(sessions_list) > 1:
            countries = set(s['country'] for s in sessions_list)
            if len(countries) > 1:
                for session_info in sessions_list:
                    issues.append({
                        "sessionId": session_info['sessionId'],
                        "issue_type": "concurrent_different_countries",
                        "severity": "high",
                        "recommendation": "Verify user identity and location"
                    })
    
    flagged_sessions = set(issue['sessionId'] for issue in issues)
    
    return {
        "issues": issues,
        "summary": {
            "total": len(sessions),
            "flagged": len(flagged_sessions)
        }
    }

def main():
    input_data = sys.stdin.read()
    sessions = json.loads(input_data)
    result = audit_sessions(sessions)
    print("issues")

if __name__ == "__main__":
    main()