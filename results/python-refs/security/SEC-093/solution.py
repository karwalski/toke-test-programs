import sys
import urllib.request
import urllib.parse
import urllib.error

def test_host_header_injection(url):
    print("Testing")
    
    # Parse the original URL to get components
    parsed = urllib.parse.urlparse(url)
    original_host = parsed.netloc
    
    # Test payloads for Host header injection
    test_hosts = [
        "evil.com",
        "attacker.example.com",
        "localhost",
        "127.0.0.1",
        original_host + ".evil.com",
        "evil.com." + original_host
    ]
    
    for test_host in test_hosts:
        try:
            # Create request with manipulated Host header
            req = urllib.request.Request(url)
            req.add_header('Host', test_host)
            req.add_header('User-Agent', 'Mozilla/5.0 (compatible; SecurityTest)')
            
            # Send request
            with urllib.request.urlopen(req, timeout=10) as response:
                response_body = response.read().decode('utf-8', errors='ignore')
                response_headers = dict(response.headers)
                
                # Check if test host is reflected in response body
                if test_host in response_body:
                    print(f"VULNERABLE with reflected host value {test_host} and impact description Host header injection - malicious host reflected in response")
                    return
                
                # Check for redirects containing the malicious host
                location = response_headers.get('Location', '')
                if location and test_host in location:
                    print(f"VULNERABLE with reflected host value {test_host} and impact description Host header injection - redirect to malicious host")
                    return
                    
        except urllib.error.HTTPError as e:
            # Check redirect responses for malicious host
            if hasattr(e, 'headers'):
                location = e.headers.get('Location', '')
                if location and test_host in location:
                    print(f"VULNERABLE with reflected host value {test_host} and impact description Host header injection - redirect to malicious host")
                    return
        except Exception:
            # Continue testing other payloads if one fails
            continue

# Read URL from stdin
url = input().strip()
test_host_header_injection(url)