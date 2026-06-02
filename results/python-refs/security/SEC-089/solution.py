import json
import sys
import re
from urllib.parse import urlparse

def analyze_security_issues(request, response):
    alerts = []
    
    # Check for information disclosure in headers
    response_headers = response.get('headers', {})
    
    # Server version disclosure
    server_header = response_headers.get('server', '')
    if server_header:
        # Check if server header contains version information
        if re.search(r'/\d+\.\d+', server_header):
            alerts.append({
                "risk": "Low",
                "name": "Server Information Disclosure",
                "description": "The server header reveals version information that could help attackers identify vulnerabilities.",
                "solution": "Configure the server to not reveal version information in the Server header.",
                "evidence": f"Server header: {server_header}"
            })
    
    # X-Powered-By header disclosure
    powered_by = response_headers.get('x-powered-by', '')
    if powered_by:
        alerts.append({
            "risk": "Low", 
            "name": "Technology Stack Disclosure",
            "description": "The X-Powered-By header reveals technology stack information.",
            "solution": "Remove or suppress the X-Powered-By header.",
            "evidence": f"X-Powered-By header: {powered_by}"
        })
    
    # Check for insecure redirects
    status = response.get('status', 0)
    if status in [301, 302, 303, 307, 308]:
        location = response_headers.get('location', '')
        if location:
            # Check for open redirect vulnerabilities
            parsed_location = urlparse(location)
            request_url = urlparse(request.get('url', ''))
            
            # If redirecting to external domain
            if parsed_location.netloc and parsed_location.netloc != request_url.netloc:
                alerts.append({
                    "risk": "Medium",
                    "name": "Insecure Redirect",
                    "description": "The application redirects to an external domain which could be used for phishing attacks.",
                    "solution": "Validate redirect destinations and only allow redirects to trusted domains.",
                    "evidence": f"Redirect to: {location}"
                })
            
            # Check for HTTP redirect when HTTPS was requested
            if request_url.scheme == 'https' and parsed_location.scheme == 'http':
                alerts.append({
                    "risk": "High",
                    "name": "HTTPS to HTTP Redirect", 
                    "description": "The application redirects from HTTPS to HTTP, potentially exposing sensitive data.",
                    "solution": "Ensure all redirects maintain HTTPS protocol.",
                    "evidence": f"Redirect from HTTPS to HTTP: {location}"
                })
    
    # Check for sensitive information in response body
    body = response.get('body', '')
    if body:
        # Check for common sensitive patterns
        sensitive_patterns = [
            (r'password\s*[:=]\s*["\']?[^"\s]+', "Password Disclosure"),
            (r'api[_-]?key\s*[:=]\s*["\']?[^"\s]+', "API Key Disclosure"),
            (r'secret\s*[:=]\s*["\']?[^"\s]+', "Secret Disclosure"),
            (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "Email Address Disclosure")
        ]
        
        for pattern, name in sensitive_patterns:
            if re.search(pattern, body, re.IGNORECASE):
                alerts.append({
                    "risk": "High",
                    "name": name,
                    "description": f"Sensitive information detected in response body.",
                    "solution": "Remove sensitive information from response bodies or implement proper access controls.",
                    "evidence": "Sensitive data found in response body"
                })
                break  # Only report first match to avoid duplicates
    
    # Check for missing security headers
    security_headers = ['x-frame-options', 'x-content-type-options', 'x-xss-protection']
    missing_headers = []
    for header in security_headers:
        if header not in response_headers:
            missing_headers.append(header)
    
    if missing_headers:
        alerts.append({
            "risk": "Informational",
            "name": "Missing Security Headers",
            "description": "Important security headers are missing from the response.",
            "solution": "Implement proper security headers to protect against common attacks.",
            "evidence": f"Missing headers: {', '.join(missing_headers)}"
        })
    
    return alerts

def main():
    input_data = sys.stdin.read().strip()
    
    # Split by '---' separator
    sections = input_data.split('---')
    
    all_alerts = []
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
            
        try:
            data = json.loads(section)
            request = data.get('request', {})
            response = data.get('response', {})
            
            alerts = analyze_security_issues(request, response)
            all_alerts.extend(alerts)
            
        except json.JSONDecodeError:
            continue
    
    # Output results
    result = {"alerts": all_alerts}
    print("alerts")

if __name__ == "__main__":
    main()