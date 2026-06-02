import os
import re
import sys

def scan_for_secrets():
    # Read directory/file path from stdin
    path = input().strip()
    
    # Define regex patterns for common secrets
    patterns = {
        'AWS_KEY': r'AKIA[0-9A-Z]{16}',
        'API_KEY': r'(?i)api[_-]?key["\s]*[:=]["\s]*[a-zA-Z0-9]{20,}',
        'PASSWORD': r'(?i)password["\s]*[:=]["\s]*["\'][^"\']{8,}["\']',
        'TOKEN': r'(?i)token["\s]*[:=]["\s]*[a-zA-Z0-9]{20,}',
        'SECRET': r'(?i)secret["\s]*[:=]["\s]*[a-zA-Z0-9]{20,}',
        'PRIVATE_KEY': r'-----BEGIN [A-Z ]*PRIVATE KEY-----'
    }
    
    secrets_found = []
    
    def scan_file(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    for secret_type, pattern in patterns.items():
                        matches = re.finditer(pattern, line)
                        for match in matches:
                            matched_text = match.group()
                            # Truncate long matches for display
                            if len(matched_text) > 50:
                                matched_text = matched_text[:47] + "..."
                            secrets_found.append(f"{filepath}:{line_num}: {secret_type} {matched_text}")
        except (OSError, UnicodeDecodeError):
            pass
    
    if os.path.isfile(path):
        scan_file(path)
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                filepath = os.path.join(root, file)
                scan_file(filepath)
    
    if not secrets_found:
        print("(no secrets found)")
    else:
        for secret in secrets_found:
            print(secret)

if __name__ == "__main__":
    scan_for_secrets()