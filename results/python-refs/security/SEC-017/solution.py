import json
import sys
import re

def check_sql_injection(request):
    url = request.get('url', '')
    body = request.get('body', '') or ''
    sql_patterns = [
        r"(\s|^|=)(or|and)\s+\d+\s*=\s*\d+",
        r"(\s|^)(or|and)\s+\'\d+\'\s*=\s*\'\d+\'",
        r"union\s+select",
        r"drop\s+table",
        r"insert\s+into",
        r"delete\s+from",
        r"update\s+.*\s+set",
        r"exec\s*\(",
        r"sp_executesql",
        r"xp_cmdshell",
        r";\s*(drop|insert|delete|update|exec)",
        r"\d+\s*=\s*\d+",
        r"'\s*or\s*'",
    ]
    combined = f"{url} {body}".lower()
    for pattern in sql_patterns:
        if re.search(pattern, combined, re.IGNORECASE):
            return {
                "owasp_id": "A03",
                "title": "Injection - SQL Injection",
                "severity": "High",
                "evidence": "Potential SQL injection pattern detected in request URL or body",
                "remediation": "Use parameterized queries, input validation, and prepared statements"
            }
    return None

def check_broken_auth(request, response):
    headers = request.get('headers', {}) or {}
    response_headers = response.get('headers', {}) or {}
    cookie_val = ""
    for k, v in headers.items():
        if k.lower() == 'cookie':
            cookie_val += str(v)
    for k, v in response_headers.items():
        if k.lower() == 'set-cookie':
            cookie_val += str(v)
    if 'sessionid=' in cookie_val.lower() and 'secure' not in cookie_val.lower():
        return {
            "owasp_id": "A07",
            "title": "Identification and Authentication Failures",
            "severity": "Medium",
            "evidence": "Insecure session cookie detected (missing Secure flag)",
            "remediation": "Use secure session management with HttpOnly and Secure flags"
        }
    return None

def check_broken_access(request, response):
    url = request.get('url', '') or ''
    status = response.get('status', 0)
    if re.search(r'\.\./', url) or re.search(r'/admin', url, re.IGNORECASE):
        if status == 200:
            return {
                "owasp_id": "A01",
                "title": "Broken Access Control",
                "severity": "High",
                "evidence": "Sensitive endpoint or path traversal accessed successfully",
                "remediation": "Enforce proper authorization checks on all endpoints"
            }
    return None

def check_sensitive_data(request, response):
    response_body = response.get('body', '') or ''
    sensitive_patterns = [
        r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        r'\b\d{3}-\d{2}-\d{4}\b',
        r'password\s*[:=]\s*["\']?[^"\'\s]+',
        r'api[_-]?key\s*[:=]\s*["\']?[^"\'\s]+',
        r'secret\s*[:=]\s*["\']?[^"\'\s]+',
    ]
    for pattern in sensitive_patterns:
        if re.search(pattern, str(response_body), re.IGNORECASE):
            return {
                "owasp_id": "A02",
                "title": "Cryptographic Failures",
                "severity": "High",
                "evidence": "Sensitive data detected in response",
                "remediation": "Encrypt sensitive data and use proper data classification"
            }
    url = request.get('url', '') or ''
    if url.lower().startswith('http://'):
        return {
            "owasp_id": "A02",
            "title": "Cryptographic Failures",
            "severity": "Medium",
            "evidence": "Plaintext HTTP used instead of HTTPS",
            "remediation": "Use HTTPS/TLS for all communications"
        }
    return None

def check_security_misconfiguration(request, response):
    response_headers = response.get('headers', {}) or {}
    header_keys_lower = [h.lower() for h in response_headers.keys()]
    security_headers = ['x-frame-options', 'content-security-policy', 'strict-transport-security']
    missing = [h for h in security_headers if h not in header_keys_lower]
    if missing:
        return {
            "owasp_id": "A05",
            "title": "Security Misconfiguration",
            "severity": "Medium",
            "evidence": f"Missing security headers: {', '.join(missing)}",
            "remediation": "Implement security headers and harden server configuration"
        }
    return None

def analyze(pair):
    findings = []
    request = pair.get('request', {}) or {}
    response = pair.get('response', {}) or {}
    for f in [
        check_broken_access(request, response),
        check_sensitive_data(request, response),
        check_sql_injection(request),
        check_security_misconfiguration(request, response),
        check_broken_auth(request, response),
    ]:
        if f:
            findings.append(f)
    return findings

def main():
    try:
        data = sys.stdin.read().strip()
        pairs = json.loads(data)
        all_findings = []
        for p in pairs:
            all_findings.extend(analyze(p))
        result = {"findings": all_findings}
        print(json.dumps(result))
    except Exception:
        print(json.dumps({"findings": []}))

if __name__ == "__main__":
    main()