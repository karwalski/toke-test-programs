import sys
import urllib.request
import urllib.parse
import ssl

def fetch_headers(url):
    try:
        # Create SSL context that doesn't verify certificates for testing
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            return dict(response.headers)
    except:
        return {}

def truncate_value(value, max_len=40):
    if len(value) > max_len:
        return value[:max_len-3] + "..."
    return value

def grade_security_headers(headers):
    security_headers = {
        'Strict-Transport-Security': {
            'weight': 20,
            'check': lambda v: 'max-age=' in v and int(v.split('max-age=')[1].split(';')[0]) >= 31536000
        },
        'Content-Security-Policy': {
            'weight': 25,
            'check': lambda v: len(v) > 10 and 'unsafe-inline' not in v
        },
        'X-Frame-Options': {
            'weight': 15,
            'check': lambda v: v.upper() in ['DENY', 'SAMEORIGIN']
        },
        'X-Content-Type-Options': {
            'weight': 10,
            'check': lambda v: v.lower() == 'nosniff'
        },
        'Referrer-Policy': {
            'weight': 10,
            'check': lambda v: v.lower() in ['no-referrer', 'strict-origin', 'strict-origin-when-cross-origin']
        },
        'Permissions-Policy': {
            'weight': 10,
            'check': lambda v: len(v) > 5
        },
        'X-XSS-Protection': {
            'weight': 5,
            'check': lambda v: '1' in v
        },
        'Cache-Control': {
            'weight': 5,
            'check': lambda v: 'no-store' in v or 'no-cache' in v
        }
    }
    
    results = []
    total_score = 0
    
    # Check case-insensitive headers
    headers_lower = {k.lower(): v for k, v in headers.items()}
    
    for header, config in security_headers.items():
        header_lower = header.lower()
        present = header_lower in headers_lower
        value = headers_lower.get(header_lower, '')
        
        if present:
            score_impact = config['weight'] if config['check'](value) else config['weight'] // 2
            total_score += score_impact
        else:
            score_impact = 0
            
        results.append({
            'header': header,
            'present': 'yes' if present else 'no',
            'value': truncate_value(value) if value else '',
            'score_impact': score_impact
        })
    
    return results, total_score

def main():
    url = input().strip()
    
    headers = fetch_headers(url)
    results, total_score = grade_security_headers(headers)
    
    print(f"{'Header':<30} {'Present':<8} {'Value':<42} {'Score'}")
    print("-" * 88)
    
    for result in results:
        print(f"{result['header']:<30} {result['present']:<8} {result['value']:<42} {result['score_impact']}")
    
    print("-" * 88)
    print(f"Score: {total_score}/100")

if __name__ == "__main__":
    main()