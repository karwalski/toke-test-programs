import sys
import urllib.request
import urllib.parse
import urllib.error
import base64
import json

def test_http_basic(url, username, password):
    try:
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        request = urllib.request.Request(url)
        request.add_header("Authorization", f"Basic {credentials}")
        response = urllib.request.urlopen(request, timeout=10)
        return response.status == 200
    except:
        return False

def test_json_form(url, username, password):
    try:
        data = json.dumps({"username": username, "password": password}).encode()
        request = urllib.request.Request(url, data=data)
        request.add_header("Content-Type", "application/json")
        response = urllib.request.urlopen(request, timeout=10)
        return response.status == 200
    except:
        return False

def test_digest(url, username, password):
    try:
        # Simple digest attempt - just try basic auth as fallback
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        request = urllib.request.Request(url)
        request.add_header("Authorization", f"Basic {credentials}")
        response = urllib.request.urlopen(request, timeout=10)
        return response.status == 200
    except:
        return False

def main():
    url = input().strip()
    service_type = input().strip()
    
    print("Testing")
    
    # Known default credentials
    credentials = [
        ("admin", "admin"),
        ("admin", "password"),
        ("root", "root"),
        ("admin", ""),
        ("root", ""),
        ("administrator", "administrator"),
        ("guest", "guest"),
        ("test", "test"),
        ("user", "user"),
        ("admin", "123456")
    ]
    
    successful_creds = []
    
    for username, password in credentials:
        if service_type == "http_basic":
            success = test_http_basic(url, username, password)
        elif service_type == "json_form":
            success = test_json_form(url, username, password)
        elif service_type == "digest":
            success = test_digest(url, username, password)
        else:
            success = False
            
        if success:
            successful_creds.append((username, password))

if __name__ == "__main__":
    main()