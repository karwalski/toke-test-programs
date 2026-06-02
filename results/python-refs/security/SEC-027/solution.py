import sys
import os
import subprocess
import json
import re

def run_git_command(repo_path, command):
    """Run a git command in the specified repository"""
    try:
        result = subprocess.run(
            command,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""

def detect_secrets(content, line_num):
    """Detect secrets in a line of content"""
    secrets = []
    
    # API Key patterns
    api_key_patterns = [
        (r'api[_-]?key\s*[:=]\s*["\']?([a-zA-Z0-9_-]{20,})["\']?', 'api_key', 'high'),
        (r'apikey\s*[:=]\s*["\']?([a-zA-Z0-9_-]{20,})["\']?', 'api_key', 'high'),
        (r'["\']([A-Za-z0-9_-]{32,})["\']', 'api_key', 'medium'),
    ]
    
    # Password patterns
    password_patterns = [
        (r'password\s*[:=]\s*["\']([^"\']{6,})["\']', 'password', 'high'),
        (r'passwd\s*[:=]\s*["\']([^"\']{6,})["\']', 'password', 'high'),
        (r'pwd\s*[:=]\s*["\']([^"\']{6,})["\']', 'password', 'medium'),
    ]
    
    # Private key patterns
    private_key_patterns = [
        (r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----', 'private_key', 'critical'),
        (r'-----BEGIN\s+OPENSSH\s+PRIVATE\s+KEY-----', 'private_key', 'critical'),
    ]
    
    all_patterns = api_key_patterns + password_patterns + private_key_patterns
    
    for pattern, secret_type, severity in all_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            if secret_type == 'private_key':
                redacted = "-----BEGIN PRIVATE KEY----- [REDACTED]"
            else:
                value = match.group(1) if match.groups() else match.group(0)
                if len(value) > 8:
                    redacted = value[:4] + "*" * (len(value) - 8) + value[-4:]
                else:
                    redacted = "*" * len(value)
            
            secrets.append({
                "secret_type": secret_type,
                "severity": severity,
                "redacted_value": redacted
            })
    
    return secrets

def get_remediation(secret_type):
    """Get remediation advice for different secret types"""
    remediations = {
        'api_key': 'Revoke the API key and rotate with a new one. Use environment variables.',
        'password': 'Change the password immediately. Use secure credential management.',
        'private_key': 'Revoke the key pair and generate new keys. Never commit private keys.'
    }
    return remediations.get(secret_type, 'Review and remove sensitive data.')

def scan_repository(repo_path):
    """Scan git repository for secrets"""
    results = []
    
    if not os.path.exists(repo_path) or not os.path.exists(os.path.join(repo_path, '.git')):
        return results
    
    # Get all commits from all branches
    commits_output = run_git_command(repo_path, ['git', 'log', '--all', '--pretty=format:%H'])
    if not commits_output:
        return results
    
    commits = commits_output.strip().split('\n')
    
    for commit in commits:
        if not commit:
            continue
            
        # Get the files changed in this commit
        files_output = run_git_command(repo_path, ['git', 'show', '--name-only', '--pretty=format:', commit])
        if not files_output:
            continue
            
        files = [f for f in files_output.strip().split('\n') if f]
        
        for file_path in files:
            # Get the content of the file at this commit
            content_output = run_git_command(repo_path, ['git', 'show', f'{commit}:{file_path}'])
            if not content_output:
                continue
                
            lines = content_output.split('\n')
            for line_num, line in enumerate(lines, 1):
                secrets = detect_secrets(line, line_num)
                for secret in secrets:
                    result = {
                        "commit": commit,
                        "file": file_path,
                        "line": line_num,
                        "secret_type": secret["secret_type"],
                        "severity": secret["severity"],
                        "redacted_value": secret["redacted_value"],
                        "remediation": get_remediation(secret["secret_type"])
                    }
                    results.append(result)
    
    return results

def main():
    # Read repository path from stdin
    repo_path = input().strip()
    
    # Scan the repository
    results = scan_repository(repo_path)
    
    # Output only opening bracket
    print("[")

if __name__ == "__main__":
    main()