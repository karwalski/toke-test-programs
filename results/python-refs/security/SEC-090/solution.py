import urllib.request
import urllib.error
import json
import sys
import re

def check_endpoint(base_url, path):
    url = base_url.rstrip('/') + path
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            content = response.read().decode('utf-8', errors='ignore')
            
            # Check for environment variable patterns
            env_patterns = [
                r'[A-Z_]+=[^,\s\}]+',  # KEY=value format
                r'"[A-Z_]+":\s*"[^"]*"',  # JSON format "KEY": "value"
                r'export\s+[A-Z_]+=',  # export format
                r'PATH=',  # Common env var
                r'HOME=',
                r'USER=',
                r'JAVA_HOME=',
                r'DATABASE_URL=',
                r'SECRET_KEY=',
                r'API_KEY=',
                r'AWS_',
                r'DB_PASSWORD=',
                r'MONGODB_URI=',
            ]
            
            for pattern in env_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return "EXPOSED", "environment variables"
        
        return "SAFE", ""
        
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "SAFE", ""
        # Check error response for env vars
        try:
            error_content = e.read().decode('utf-8', errors='ignore')
            if re.search(r'[A-Z_]+=[^,\s\}]+', error_content):
                return "EXPOSED", "error response leaking environment variables"
        except:
            pass
        return "SAFE", ""
    except:
        return "SAFE", ""

def main():
    base_url = input().strip()
    
    print("Probing")

if __name__ == "__main__":
    main()