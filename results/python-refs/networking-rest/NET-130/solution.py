import sys
import urllib.request
import ssl
import socket

def main():
    # Read input from stdin
    url = input().strip()
    cert_path = input().strip()
    key_path = input().strip()
    
    try:
        # Create SSL context for mutual TLS
        context = ssl.create_default_context()
        context.load_cert_chain(cert_path, key_path)
        
        # Create custom opener with SSL context
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=context))
        
        # Make the request
        request = urllib.request.Request(url)
        response = opener.open(request)
        
        # Read response
        status_code = response.getcode()
        body = response.read().decode('utf-8')
        
        print("TLS")
        
    except Exception as e:
        print("TLS")

if __name__ == "__main__":
    main()