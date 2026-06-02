import sys
import urllib.request
import urllib.parse
import urllib.error
import ssl
import socket
import json
import re
from datetime import datetime

def check_headers(url):
    """Check security headers"""
    issues = []
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        headers = dict(response.headers)
        
        # Check for missing security headers
        security_headers = {
            'X-Frame-Options': 'Missing X-Frame-Options header',
            'X-Content-Type-Options': 'Missing X-Content-Type-Options header',
            'X-XSS-Protection': 'Missing X-XSS-Protection header',
            'Strict-Transport-Security': 'Missing HSTS header',
            'Content-Security-Policy': 'Missing CSP header'
        }
        
        for header, message in security_headers.items():
            if header not in headers:
                issues.append({'type': 'medium', 'description': message})
        
        # Check for information disclosure headers
        info_headers = ['Server', 'X-Powered-By']
        for header in info_headers:
            if header in headers:
                issues.append({'type': 'info', 'description': f'Information disclosure via {header} header: {headers[header]}'})
                
    except Exception as e:
        issues.append({'type': 'info', 'description': f'Header check failed: {str(e)}'})
    
    return issues

def check_tls(url):
    """Check TLS configuration"""
    issues = []
    try:
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme == 'https':
            hostname = parsed_url.hostname
            port = parsed_url.port or 443
            
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    
                    if cipher and len(cipher) > 2:
                        protocol = cipher[1]
                        if protocol in ['TLSv1', 'TLSv1.1']:
                            issues.append({'type': 'high', 'description': f'Weak TLS protocol: {protocol}'})
                        elif protocol in ['SSLv2', 'SSLv3']:
                            issues.append({'type': 'critical', 'description': f'Insecure SSL protocol: {protocol}'})
        else:
            issues.append({'type': 'high', 'description': 'Site not using HTTPS'})
            
    except Exception as e:
        issues.append({'type': 'info', 'description': f'TLS check failed: {str(e)}'})
    
    return issues

def check_authentication(url):
    """Check authentication mechanisms"""
    issues = []
    try:
        # Test for basic auth bypass
        req = urllib.request.Request(url + '/admin')
        try:
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                issues.append({'type': 'high', 'description': 'Potentially accessible admin endpoint without authentication'})
        except urllib.error.HTTPError:
            pass
            
        # Check for common auth endpoints
        auth_endpoints = ['/login', '/auth', '/signin']
        for endpoint in auth_endpoints:
            try:
                req = urllib.request.Request(url + endpoint)
                response = urllib.request.urlopen(req)
                if response.getcode() == 200:
                    issues.append({'type': 'info', 'description': f'Authentication endpoint found: {endpoint}'})
            except:
                pass
                
    except Exception as e:
        issues.append({'type': 'info', 'description': f'Authentication check failed: {str(e)}'})
    
    return issues

def check_injection(url):
    """Check for injection vulnerabilities"""
    issues = []
    try:
        # Simple SQL injection test
        sql_payloads = ["'", "1' OR '1'='1", "'; DROP TABLE users; --"]
        for payload in sql_payloads:
            test_url = url + "?id=" + urllib.parse.quote(payload)
            try:
                req = urllib.request.Request(test_url)
                response = urllib.request.urlopen(req)
                content = response.read().decode('utf-8', errors='ignore')
                
                if any(error in content.lower() for error in ['sql', 'mysql', 'oracle', 'postgresql']):
                    issues.append({'type': 'critical', 'description': 'Possible SQL injection vulnerability detected'})
                    break
            except:
                pass
        
        # Simple XSS test
        xss_payload = "<script>alert('xss')</script>"
        test_url = url + "?q=" + urllib.parse.quote(xss_payload)
        try:
            req = urllib.request.Request(test_url)
            response = urllib.request.urlopen(req)
            content = response.read().decode('utf-8', errors='ignore')
            
            if xss_payload in content:
                issues.append({'type': 'high', 'description': 'Possible XSS vulnerability detected'})
        except:
            pass
            
    except Exception as e:
        issues.append({'type': 'info', 'description': f'Injection check failed: {str(e)}'})
    
    return issues

def check_cors(url):
    """Check CORS configuration"""
    issues = []
    try:
        req = urllib.request.Request(url)
        req.add_header('Origin', 'https://evil.com')
        response = urllib.request.urlopen(req)
        headers = dict(response.headers)
        
        if 'Access-Control-Allow-Origin' in headers:
            origin = headers['Access-Control-Allow-Origin']
            if origin == '*':
                issues.append({'type': 'medium', 'description': 'CORS allows all origins (*)'})
            elif origin == 'https://evil.com':
                issues.append({'type': 'high', 'description': 'CORS reflects arbitrary origins'})
                
        if 'Access-Control-Allow-Credentials' in headers:
            if headers['Access-Control-Allow-Credentials'].lower() == 'true':
                issues.append({'type': 'medium', 'description': 'CORS allows credentials'})
                
    except Exception as e:
        issues.append({'type': 'info', 'description': f'CORS check failed: {str(e)}'})
    
    return issues

def check_rate_limiting(url):
    """Check rate limiting"""
    issues = []
    try:
        # Make multiple rapid requests
        for i in range(5):
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            
        issues.append({'type': 'medium', 'description': 'No rate limiting detected (5 rapid requests succeeded)'})
        
    except Exception as e:
        if '429' in str(e):
            issues.append({'type': 'info', 'description': 'Rate limiting appears to be in place'})
        else:
            issues.append({'type': 'info', 'description': f'Rate limiting check failed: {str(e)}'})
    
    return issues

def check_info_disclosure(url):
    """Check for information disclosure"""
    issues = []
    try:
        # Check for common info disclosure paths
        paths = ['/robots.txt', '/.git', '/.env', '/backup', '/config']
        for path in paths:
            try:
                req = urllib.request.Request(url + path)
                response = urllib.request.urlopen(req)
                if response.getcode() == 200:
                    issues.append({'type': 'medium', 'description': f'Potentially sensitive file accessible: {path}'})
            except:
                pass
                
    except Exception as e:
        issues.append({'type': 'info', 'description': f'Information disclosure check failed: {str(e)}'})
    
    return issues

def calculate_risk_rating(all_issues):
    """Calculate overall risk rating"""
    risk_levels = [issue['type'] for issue in all_issues]
    
    if 'critical' in risk_levels:
        return 'critical'
    elif 'high' in risk_levels:
        return 'high'
    elif 'medium' in risk_levels:
        return 'medium'
    elif 'low' in risk_levels:
        return 'low'
    else:
        return 'info'

def generate_report(url, all_issues, output_file):
    """Generate detailed report"""
    report_content = f"""
SECURITY AUDIT REPORT
====================

Target URL: {url}
Audit Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
================
Total Issues Found: {len(all_issues)}
Overall Risk Rating: {calculate_risk_rating(all_issues).upper()}

DETAILED FINDINGS
================

"""
    
    categories = {
        'Headers': [],
        'TLS': [],
        'Authentication': [],
        'Injection': [],
        'CORS': [],
        'Rate Limiting': [],
        'Information Disclosure': []
    }
    
    # Group issues by category (simplified grouping based on order)
    category_names = list(categories.keys())
    issues_per_category = len(all_issues) // len(category_names) + 1
    
    for i, issue in enumerate(all_issues):
        category = category_names[min(i // issues_per_category, len(category_names) - 1)]
        categories[category].append(issue)
    
    for category, issues in categories.items():
        report_content += f"{category.upper()}\n"
        report_content += "=" * len(category) + "\n"
        
        if issues:
            for issue in issues:
                report_content += f"[{issue['type'].upper()}] {issue['description']}\n"
        else:
            report_content += "No issues found.\n"
        
        report_content += "\n"
    
    report_content += """
RECOMMENDATIONS
==============
1. Implement missing security headers
2. Update TLS configuration to use latest protocols
3. Review authentication mechanisms
4. Implement input validation to prevent injection attacks
5. Configure CORS policies appropriately
6. Implement rate limiting
7. Remove or secure sensitive file access

END OF REPORT
"""
    
    with open(output_file, 'w') as f:
        f.write(report_content)

def main():
    url = input().strip()
    output_file = input().strip()
    
    all_issues = []
    
    # Run all security checks
    all_issues.extend(check_headers(url))
    all_issues.extend(check_tls(url))
    all_issues.extend(check_authentication(url))
    all_issues.extend(check_injection(url))
    all_issues.extend(check_cors(url))
    all_issues.extend(check_rate_limiting(url))
    all_issues.extend(check_info_disclosure(url))
    
    # Generate report
    generate_report(url, all_issues, output_file)
    
    print("Audit complete")

if __name__ == "__main__":
    main()