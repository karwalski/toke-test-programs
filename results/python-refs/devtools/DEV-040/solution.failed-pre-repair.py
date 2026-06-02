import sys
import re

def scan_for_secrets(file_path):
    patterns = {
        'API_KEY': [
            r'(?i)api[_-]?key\s*[:=]\s*["\']?([A-Z0-9]{20,})["\']?',
            r'(?i)apikey\s*[:=]\s*["\']?([A-Z0-9]{20,})["\']?',
            r'["\']?(AKIA[0-9A-Z]{16})["\']?',  # AWS Access Key
            r'["\']?(sk-[a-zA-Z0-9]{48})["\']?'  # OpenAI API Key
        ],
        'PASSWORD': [
            r'(?i)password\s*[:=]\s*["\']([^"\']{8,})["\']',
            r'(?i)passwd\s*[:=]\s*["\']([^"\']{8,})["\']'
        ],
        'SECRET': [
            r'(?i)secret\s*[:=]\s*["\']([A-Za-z0-9+/=]{20,})["\']',
            r'(?i)secret[_-]?key\s*[:=]\s*["\']([A-Za-z0-9+/=]{20,})["\']'
        ],
        'TOKEN': [
            r'(?i)token\s*[:=]\s*["\']([A-Za-z0-9+/=]{20,})["\']',
            r'(?i)access[_-]?token\s*[:=]\s*["\']([A-Za-z0-9+/=]{20,})["\']'
        ]
    }
    
    findings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for secret_type, pattern_list in patterns.items():
                    for pattern in pattern_list:
                        matches = re.finditer(pattern, line)
                        for match in matches:
                            secret_value = match.group(1)
                            if len(secret_value) >= 8:  # Minimum length check
                                redacted = secret_value[:3] + '...redacted'
                                findings.append(f"{file_path}:{line_num}: [{secret_type}] {redacted}")
    except (IOError, OSError):
        pass
    
    return findings

def main():
    for line in sys.stdin:
        file_path = line.strip()
        if file_path:
            findings = scan_for_secrets(file_path)
            for finding in findings:
                print(finding)

if __name__ == "__main__":
    main()