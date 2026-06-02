import sys
import urllib.request
import urllib.parse
import json
import ssl

def check_hsts_preload_list(domain):
    """Check if domain is on Chrome's HSTS preload list"""
    try:
        # Chrome's HSTS preload list API
        url = f"https://hstspreload.org/api/v2/status?domain={domain}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get('preloaded', False)
    except:
        return False

def get_hsts_header(domain):
    """Get HSTS header from domain"""
    try:
        url = f"https://{domain}/"
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (HSTS Checker)')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.headers.get('Strict-Transport-Security', '')
    except:
        return ''

def parse_hsts_header(header):
    """Parse HSTS header and extract values"""
    if not header:
        return None, False, False
    
    max_age = None
    include_subdomains = False
    preload = False
    
    # Split by semicolon and parse each directive
    directives = [d.strip() for d in header.split(';')]
    
    for directive in directives:
        if directive.startswith('max-age='):
            try:
                max_age = int(directive.split('=', 1)[1])
            except:
                max_age = 0
        elif directive.lower() == 'includesubdomains':
            include_subdomains = True
        elif directive.lower() == 'preload':
            preload = True
    
    return max_age, include_subdomains, preload

def calculate_grade(hsts_enabled, max_age, include_subdomains, preload, preload_list_status, issues):
    """Calculate HSTS grade"""
    if not hsts_enabled:
        return 'F'
    
    if len(issues) > 2:
        return 'D'
    elif len(issues) > 1:
        return 'C'
    elif len(issues) == 1:
        return 'B'
    elif preload_list_status and preload and include_subdomains and max_age >= 31536000:
        return 'A+'
    elif max_age >= 31536000 and include_subdomains:
        return 'A'
    else:
        return 'B'

def main():
    domain = input().strip()
    
    # Get HSTS header
    hsts_header = get_hsts_header(domain)
    hsts_enabled = bool(hsts_header)
    
    # Parse header
    max_age, include_subdomains, preload = parse_hsts_header(hsts_header)
    
    # Check preload list
    preload_list_status = check_hsts_preload_list(domain)
    
    # Identify issues
    issues = []
    if not hsts_enabled:
        issues.append("HSTS header not present")
    else:
        if max_age is None or max_age < 86400:
            issues.append("max-age too low (should be at least 86400)")
        if not include_subdomains:
            issues.append("includeSubDomains directive missing")
        if not preload:
            issues.append("preload directive missing")
    
    if not preload_list_status:
        issues.append("Domain not on HSTS preload list")
    
    # Calculate grade
    grade = calculate_grade(hsts_enabled, max_age, include_subdomains, preload, preload_list_status, issues)
    
    print("hstsEnabled")

if __name__ == "__main__":
    main()