import sys
import json
import ssl
import socket
import urllib.parse

def test_certificate_pinning(url):
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname
    port = parsed.port or 443
    
    result = {
        "url": url,
        "certificatePinningDetected": False,
        "method": "",
        "details": ""
    }
    
    try:
        # Create SSL context that ignores certificate verification
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Try to connect with invalid certificate handling
        sock = socket.create_connection((hostname, port), timeout=10)
        try:
            ssl_sock = context.wrap_socket(sock, server_hostname=hostname)
            ssl_sock.close()
            # If we get here, the connection was accepted despite invalid cert handling
            result["method"] = "accepted"
            result["details"] = "Connection accepted with disabled certificate verification"
            result["certificatePinningDetected"] = False
        except ssl.SSLError as e:
            result["method"] = "tls_error"
            result["details"] = str(e)
            result["certificatePinningDetected"] = True
        finally:
            sock.close()
            
    except ConnectionRefusedError as e:
        result["method"] = "connection_refused"
        result["details"] = str(e)
        result["certificatePinningDetected"] = False
    except Exception as e:
        result["method"] = "tls_error"
        result["details"] = str(e)
        result["certificatePinningDetected"] = True
    
    return result

def main():
    url = sys.stdin.readline().strip()
    result = test_certificate_pinning(url)
    
    if result["certificatePinningDetected"]:
        print("certificatePinningDetected")
    else:
        print(json.dumps(result))

if __name__ == "__main__":
    main()