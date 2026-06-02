import sys
import json
import re
import os

def analyze_log_line(line, line_num):
    """Analyze a log line for security patterns and return findings"""
    findings = []
    
    # Extract timestamp (common log formats)
    timestamp_patterns = [
        r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})',  # ISO format
        r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})',      # Syslog format
        r'(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})',      # Apache format
    ]
    
    timestamp = "unknown"
    for pattern in timestamp_patterns:
        match = re.search(pattern, line)
        if match:
            timestamp = match.group(1)
            break
    
    # 1. Privilege escalation patterns
    priv_patterns = [
        (r'sudo\s+su\s*-', 'critical', 'privilege_escalation', 'Direct root escalation via sudo su detected'),
        (r'sudo\s+-i', 'warn', 'privilege_escalation', 'Interactive sudo session initiated'),
        (r'su\s+-\s+root', 'warn', 'privilege_escalation', 'Direct root login attempt'),
        (r'passwd\s+root', 'critical', 'privilege_escalation', 'Root password change attempt'),
        (r'usermod.*-G.*wheel', 'warn', 'privilege_escalation', 'User added to wheel group'),
        (r'usermod.*-G.*sudo', 'warn', 'privilege_escalation', 'User added to sudo group'),
    ]
    
    # 2. Suspicious commands (curl|wget piped to bash)
    suspicious_cmd_patterns = [
        (r'curl.*\|.*bash', 'critical', 'suspicious_command', 'Remote script execution via curl pipe to bash'),
        (r'wget.*\|.*bash', 'critical', 'suspicious_command', 'Remote script execution via wget pipe to bash'),
        (r'curl.*\|.*sh', 'critical', 'suspicious_command', 'Remote script execution via curl pipe to shell'),
        (r'wget.*\|.*sh', 'critical', 'suspicious_command', 'Remote script execution via wget pipe to shell'),
        (r'curl.*>\s*/tmp/.*\.sh', 'warn', 'suspicious_command', 'Script downloaded to temp directory'),
        (r'wget.*>\s*/tmp/.*\.sh', 'warn', 'suspicious_command', 'Script downloaded to temp directory'),
    ]
    
    # 3. File permission changes
    permission_patterns = [
        (r'chmod\s+777', 'critical', 'file_permissions', 'Dangerous 777 permissions set - full access for all users'),
        (r'chmod\s+\+s', 'critical', 'file_permissions', 'SUID bit set - potential privilege escalation risk'),
        (r'chmod\s+4755', 'warn', 'file_permissions', 'SUID permissions set on file'),
        (r'chmod.*\+x.*/(bin|sbin)/', 'warn', 'file_permissions', 'Executable permissions set in system directory'),
        (r'chown\s+root:', 'info', 'file_permissions', 'File ownership changed to root'),
    ]
    
    # 4. Cron modifications
    cron_patterns = [
        (r'crontab\s+-e', 'warn', 'cron_modification', 'Crontab edited - review scheduled tasks'),
        (r'crontab.*-u.*root', 'critical', 'cron_modification', 'Root crontab modified - verify legitimate changes'),
        (r'/etc/crontab', 'warn', 'cron_modification', 'System crontab accessed'),
        (r'/etc/cron\.(daily|weekly|monthly)', 'warn', 'cron_modification', 'System cron directory accessed'),
        (r'echo.*>.*cron', 'critical', 'cron_modification', 'Direct cron file modification detected'),
    ]
    
    all_patterns = [
        (priv_patterns, 'privilege_escalation'),
        (suspicious_cmd_patterns, 'suspicious_command'),
        (permission_patterns, 'file_permissions'),
        (cron_patterns, 'cron_modification')
    ]
    
    for pattern_group, default_event_type in all_patterns:
        for pattern, severity, event_type, recommendation in pattern_group:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append({
                    "timestamp": timestamp,
                    "severity": severity,
                    "event_type": event_type,
                    "line": line.strip(),
                    "recommendation": recommendation
                })
    
    return findings

def main():
    try:
        # Read log file path from stdin
        log_path = input().strip()
        
        # Check if file exists
        if not os.path.exists(log_path):
            print("[]")
            return
        
        all_findings = []
        
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    findings = analyze_log_line(line, line_num)
                    all_findings.extend(findings)
        
        except (IOError, OSError):
            # If we can't read the file, return empty array
            print("[]")
            return
        
        # Output JSON array
        print(json.dumps(all_findings, indent=0, separators=(',', ':')))
        
    except EOFError:
        print("[]")
    except Exception:
        print("[]")

if __name__ == "__main__":
    main()