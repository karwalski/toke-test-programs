import sys
import urllib.request
import urllib.error
import json

def check_clickjacking_protection(url):
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        with urllib.request.urlopen(req) as response:
            headers = response.headers
            
            # Check X-Frame-Options header
            x_frame_options = headers.get('X-Frame-Options', '').strip()
            if x_frame_options:
                x_frame_options_lower = x_frame_options.lower()
                if x_frame_options_lower in ['deny', 'sameorigin'] or x_frame_options_lower.startswith('allow-from'):
                    return {
                        'url': url,
                        'protected': True,
                        'method': 'X-Frame-Options',
                        'value': x_frame_options,
                        'vulnerable': False,
                        'recommendation': 'Already protected by X-Frame-Options header'
                    }
            
            # Check Content-Security-Policy header for frame-ancestors
            csp = headers.get('Content-Security-Policy', '').strip()
            if csp:
                # Parse CSP directives
                directives = [d.strip() for d in csp.split(';') if d.strip()]
                for directive in directives:
                    parts = directive.split()
                    if parts and parts[0].lower() == 'frame-ancestors':
                        if len(parts) > 1:
                            value = ' '.join(parts[1:])
                            if "'none'" in value or "'self'" in value or any(not v.startswith("'") for v in parts[1:] if v != "'unsafe-inline'" and v != "'unsafe-eval'"):
                                return {
                                    'url': url,
                                    'protected': True,
                                    'method': 'CSP',
                                    'value': directive,
                                    'vulnerable': False,
                                    'recommendation': 'Already protected by Content-Security-Policy frame-ancestors directive'
                                }
            
            # No protection found
            return {
                'url': url,
                'protected': False,
                'method': 'none',
                'value': '',
                'vulnerable': True,
                'recommendation': 'Add X-Frame-Options: DENY or Content-Security-Policy: frame-ancestors \'none\''
            }
            
    except Exception as e:
        return {
            'url': url,
            'protected': False,
            'method': 'none',
            'value': '',
            'vulnerable': True,
            'recommendation': f'Error checking protection: {str(e)}'
        }

def main():
    url = input().strip()
    result = check_clickjacking_protection(url)
    
    if result['protected']:
        print('protected')
    else:
        print(json.dumps(result))

if __name__ == '__main__':
    main()