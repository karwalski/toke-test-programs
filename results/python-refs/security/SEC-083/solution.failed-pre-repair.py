import json
import urllib.request
import urllib.error
import ssl
import socket
from urllib.parse import urljoin

def check_https(url):
    """Check if API uses HTTPS"""
    return url.startswith('https://')

def check_ssl_certificate(url):
    """Check SSL certificate validity"""
    if not url.startswith('https://'):
        return False
    
    try:
        # Extract hostname and port
        from urllib.parse import urlparse
        parsed = urlparse(url)
        hostname = parsed.hostname
        port = parsed.port or 443
        
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                return True
    except:
        return False

def make_request(url, method='GET', headers=None):
    """Make HTTP request and return response"""
    try:
        req = urllib.request.Request(url, method=method)
        if headers:
            for key, value in headers.items():
                req.add_header(key, value)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return {
                'status_code': response.getcode(),
                'headers': dict(response.headers),
                'body': response.read().decode('utf-8', errors='ignore')
            }
    except urllib.error.HTTPError as e:
        return {
            'status_code': e.code,
            'headers': dict(e.headers) if e.headers else {},
            'body': e.read().decode('utf-8', errors='ignore') if hasattr(e, 'read') else ''
        }
    except:
        return None

def check_auth_security(base_url):
    """Check authentication security"""
    score = 0
    issues = []
    
    # Test for basic auth requirements
    response = make_request(base_url)
    if response and response['status_code'] == 401:
        score += 30
    else:
        issues.append("No authentication required")
    
    # Test for API key requirements
    test_endpoints = ['/', '/api', '/v1', '/users', '/admin']
    for endpoint in test_endpoints:
        url = urljoin(base_url, endpoint)
        resp = make_request(url)
        if resp and resp['status_code'] in [401, 403]:
            score += 10
            break
    else:
        issues.append("No API key protection detected")
    
    # Check for auth headers in response
    if response and response.get('headers'):
        auth_headers = ['www-authenticate', 'authorization']
        if any(header in response['headers'] for header in auth_headers):
            score += 20
    
    return min(score, 100), issues

def check_transport_security(base_url):
    """Check transport layer security"""
    score = 0
    issues = []
    
    # HTTPS check
    if check_https(base_url):
        score += 50
    else:
        issues.append("API does not use HTTPS")
    
    # SSL certificate check
    if check_ssl_certificate(base_url):
        score += 30
    else:
        if base_url.startswith('https://'):
            issues.append("Invalid SSL certificate")
    
    # HSTS check
    response = make_request(base_url)
    if response and response.get('headers'):
        if 'strict-transport-security' in response['headers']:
            score += 20
        else:
            issues.append("Missing HSTS header")
    
    return min(score, 100), issues

def check_security_headers(base_url):
    """Check security headers"""
    score = 0
    issues = []
    
    response = make_request(base_url)
    if not response:
        issues.append("Could not retrieve headers")
        return 0, issues
    
    headers = response.get('headers', {})
    
    # Convert headers to lowercase for case-insensitive checking
    headers_lower = {k.lower(): v for k, v in headers.items()}
    
    security_headers = {
        'x-frame-options': 15,
        'x-content-type-options': 15,
        'x-xss-protection': 15,
        'content-security-policy': 20,
        'referrer-policy': 10,
        'permissions-policy': 10,
        'strict-transport-security': 15
    }
    
    for header, points in security_headers.items():
        if header in headers_lower:
            score += points
        else:
            issues.append(f"Missing {header} header")
    
    return min(score, 100), issues

def check_rate_limiting(base_url):
    """Check rate limiting implementation"""
    score = 0
    issues = []
    
    # Make multiple rapid requests
    responses = []
    for i in range(10):
        resp = make_request(base_url)
        if resp:
            responses.append(resp)
    
    if not responses:
        issues.append("Could not test rate limiting")
        return 0, issues
    
    # Check for rate limit headers
    rate_limit_headers = ['x-ratelimit-limit', 'x-ratelimit-remaining', 'x-rate-limit-limit', 'rate-limit']
    for resp in responses:
        headers_lower = {k.lower(): v for k, v in resp.get('headers', {}).items()}
        if any(header in headers_lower for header in rate_limit_headers):
            score += 50
            break
    else:
        issues.append("No rate limiting headers detected")
    
    # Check for 429 status codes
    status_codes = [resp['status_code'] for resp in responses]
    if 429 in status_codes:
        score += 50
    else:
        issues.append("No rate limiting enforcement detected")
    
    return min(score, 100), issues

def check_input_validation(base_url):
    """Check input validation"""
    score = 0
    issues = []
    
    # Test various malicious inputs
    test_payloads = [
        "' OR '1'='1",  # SQL injection
        "<script>alert('xss')</script>",  # XSS
        "../../../etc/passwd",  # Path traversal
        "$(rm -rf /)",  # Command injection
    ]
    
    validation_detected = False
    
    for payload in test_payloads:
        # Try as query parameter
        test_url = f"{base_url}?test={payload}"
        resp = make_request(test_url)
        
        if resp and resp['status_code'] == 400:
            validation_detected = True
            score += 25
            break
    
    if not validation_detected:
        issues.append("No input validation detected for malicious payloads")
    
    # Check for proper error codes on malformed requests
    malformed_url = f"{base_url}?malformed=value&"
    resp = make_request(malformed_url)
    if resp and resp['status_code'] in [400, 422]:
        score += 25
    
    return min(score, 100), issues

def check_error_handling(base_url):
    """Check error handling security"""
    score = 0
    issues = []
    
    # Test non-existent endpoints
    test_url = urljoin(base_url, "/nonexistent/endpoint/12345")
    resp = make_request(test_url)
    
    if resp:
        if resp['status_code'] == 404:
            score += 30
        
        # Check if error response contains sensitive information
        body = resp.get('body', '').lower()
        sensitive_keywords = ['stack trace', 'exception', 'error:', 'warning:', 'debug', 'sql']
        
        if any(keyword in body for keyword in sensitive_keywords):
            issues.append("Error responses may contain sensitive information")
        else:
            score += 40
        
        # Check for proper content type in error responses
        headers = resp.get('headers', {})
        content_type = headers.get('content-type', '').lower()
        if 'application/json' in content_type:
            score += 30
    
    return min(score, 100), issues

def calculate_overall_grade(score):
    """Calculate letter grade from numeric score"""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

def generate_recommendations(all_issues):
    """Generate security recommendations based on issues"""
    recommendations = []
    
    issue_text = ' '.join(all_issues).lower()
    
    if 'https' in issue_text:
        recommendations.append("Implement HTTPS encryption for all API endpoints")
    
    if 'authentication' in issue_text or 'api key' in issue_text:
        recommendations.append("Implement proper authentication mechanisms (API keys, OAuth, JWT)")
    
    if 'header' in issue_text:
        recommendations.append("Add security headers (HSTS, CSP, X-Frame-Options, etc.)")
    
    if 'rate limiting' in issue_text:
        recommendations.append("Implement rate limiting to prevent abuse")
    
    if 'input validation' in issue_text:
        recommendations.append("Add comprehensive input validation and sanitization")
    
    if 'error' in issue_text or 'sensitive' in issue_text:
        recommendations.append("Implement secure error handling without information disclosure")
    
    if 'ssl' in issue_text or 'certificate' in issue_text:
        recommendations.append("Ensure valid SSL/TLS certificates are properly configured")
    
    if not recommendations:
        recommendations.append("Continue monitoring and regular security assessments")
    
    return recommendations

def main():
    # Read API base URL from stdin
    base_url = input().strip()
    
    # Run security checks
    auth_score, auth_issues = check_auth_security(base_url)
    transport_score, transport_issues = check_transport_security(base_url)
    headers_score, headers_issues = check_security_headers(base_url)
    rate_limit_score, rate_limit_issues = check_rate_limiting(base_url)
    input_validation_score, input_validation_issues = check_input_validation(base_url)
    error_handling_score, error_handling_issues = check_error_handling(base_url)
    
    # Calculate overall score
    overall_score = round((auth_score + transport_score + headers_score + 
                          rate_limit_score + input_validation_score + error_handling_score) / 6, 1)
    
    overall_grade = calculate_overall_grade(overall_score)
    
    # Collect all issues
    all_issues = (auth_issues + transport_issues + headers_issues + 
                 rate_limit_issues + input_validation_issues + error_handling_issues)
    
    # Generate recommendations
    recommendations = generate_recommendations(all_issues)
    
    # Create scorecard
    scorecard = {
        "url": base_url,
        "overallGrade": overall_grade,
        "overallScore": overall_score,
        "categories": {
            "auth": auth_score,
            "transport": transport_score,
            "headers": headers_score,
            "rateLimit": rate_limit_score,
            "inputValidation": input_validation_score,
            "errorHandling": error_handling_score
        },
        "issues": all_issues,
        "recommendations": recommendations
    }
    
    # Output JSON scorecard
    print(json.dumps(scorecard))

if __name__ == "__main__":
    main()