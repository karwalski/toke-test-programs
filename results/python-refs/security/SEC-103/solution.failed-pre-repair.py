import sys
import socket
import urllib.request
import urllib.error

def check_subdomain_takeover(subdomain):
    try:
        # Check if DNS resolves
        socket.gethostbyname(subdomain)
    except socket.gaierror:
        return "DANGLING_DNS"
    
    try:
        # Try to fetch the page
        response = urllib.request.urlopen(f"http://{subdomain}", timeout=5)
        content = response.read().decode('utf-8', errors='ignore').lower()
        
        # Check for common takeover indicators
        takeover_patterns = {
            'github': ['there isn\'t a github pages site here', 'repository not found'],
            'heroku': ['no such app', 'heroku | no such app'],
            'aws': ['nosuchbucket', 'bucketdoesnotexist'],
            's3': ['nosuchbucket', 'bucketdoesnotexist'],
            'azure': ['page not found', 'web app - unavailable'],
            'netlify': ['not found', 'page not found'],
            'surge': ['project not found'],
            'tumblr': ['whatever you were looking for doesn\'t currently exist'],
            'wordpress': ['do you want to register'],
            'shopify': ['sorry, this shop is currently unavailable']
        }
        
        for platform, patterns in takeover_patterns.items():
            for pattern in patterns:
                if pattern in content:
                    return f"VULNERABLE ({platform})"
        
        return "SAFE"
        
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "DANGLING_DNS"
        return "SAFE"
    except:
        return "SAFE"

def main():
    for line in sys.stdin:
        subdomain = line.strip()
        if subdomain:
            result = check_subdomain_takeover(subdomain)
            print(result)

if __name__ == "__main__":
    main()