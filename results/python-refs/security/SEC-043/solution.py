import sys
import json
import re

def scan_for_sensitive_data(content_type, body):
    findings = []
    
    # Credit card pattern (basic Luhn-valid cards like 4111111111111111)
    cc_pattern = r'\b(?:4\d{15}|5[1-5]\d{14}|3[47]\d{13}|6(?:011|5\d{2})\d{12})\b'
    
    # SSN pattern
    ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    
    # Check for credit cards
    cc_matches = re.finditer(cc_pattern, body)
    for match in cc_matches:
        redacted = match.group()[:4] + '*' * (len(match.group()) - 8) + match.group()[-4:]
        findings.append({
            "type": "credit_card",
            "severity": "high",
            "redacted_sample": redacted,
            "location": f"position {match.start()}-{match.end()}"
        })
    
    # Check for SSNs
    ssn_matches = re.finditer(ssn_pattern, body)
    for match in ssn_matches:
        redacted = "***-**-" + match.group()[-4:]
        findings.append({
            "type": "ssn",
            "severity": "high", 
            "redacted_sample": redacted,
            "location": f"position {match.start()}-{match.end()}"
        })
    
    # Check for emails
    email_matches = re.finditer(email_pattern, body)
    for match in email_matches:
        email = match.group()
        at_pos = email.find('@')
        redacted = email[:2] + '*' * (at_pos - 2) + email[at_pos:]
        findings.append({
            "type": "email",
            "severity": "medium",
            "redacted_sample": redacted,
            "location": f"position {match.start()}-{match.end()}"
        })
    
    return findings

def main():
    lines = sys.stdin.read().strip().split('\n')
    content_type = lines[0]
    body = '\n'.join(lines[1:])
    
    findings = scan_for_sensitive_data(content_type, body)
    
    if findings:
        print(findings[0]["type"])

if __name__ == "__main__":
    main()