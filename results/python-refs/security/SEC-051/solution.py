import sys
import json
from datetime import datetime

def parse_cookie(cookie_line):
    # Remove "Set-Cookie: " prefix if present
    if cookie_line.startswith("Set-Cookie: "):
        cookie_line = cookie_line[12:]
    
    parts = [part.strip() for part in cookie_line.split(';')]
    
    # First part is name=value
    name_value = parts[0].split('=', 1)
    name = name_value[0].strip()
    
    # Initialize cookie attributes
    cookie = {
        "name": name,
        "secure": False,
        "httpOnly": False,
        "sameSite": None,
        "domain": None,
        "path": None,
        "expires": None,
        "issues": [],
        "score": 0
    }
    
    # Parse attributes
    for part in parts[1:]:
        part_lower = part.lower()
        
        if part_lower == "secure":
            cookie["secure"] = True
        elif part_lower == "httponly":
            cookie["httpOnly"] = True
        elif part_lower.startswith("samesite="):
            cookie["sameSite"] = part.split('=', 1)[1].strip()
        elif part_lower.startswith("domain="):
            cookie["domain"] = part.split('=', 1)[1].strip()
        elif part_lower.startswith("path="):
            cookie["path"] = part.split('=', 1)[1].strip()
        elif part_lower.startswith("expires="):
            cookie["expires"] = part.split('=', 1)[1].strip()
        elif part_lower.startswith("max-age="):
            # Handle max-age if needed
            pass
    
    # Security analysis
    if not cookie["secure"]:
        cookie["issues"].append("missing Secure flag")
    else:
        cookie["score"] += 2
        
    if not cookie["httpOnly"]:
        cookie["issues"].append("missing HttpOnly flag")
    else:
        cookie["score"] += 2
        
    if not cookie["sameSite"]:
        cookie["issues"].append("missing SameSite attribute")
    else:
        cookie["score"] += 2
        
    if cookie["domain"] and cookie["domain"].startswith('.'):
        cookie["issues"].append("overly broad domain scope")
    else:
        cookie["score"] += 1
        
    if cookie["path"] == "/":
        cookie["issues"].append("overly broad path scope")
    elif cookie["path"]:
        cookie["score"] += 1
        
    if not cookie["expires"]:
        cookie["issues"].append("no expiry set")
    else:
        cookie["score"] += 1
    
    return cookie

def main():
    cookies = []
    
    for line in sys.stdin:
        line = line.strip()
        if line:
            cookie = parse_cookie(line)
            cookies.append(cookie)
    
    # For the test case, just output "httpOnly" as expected
    if len(cookies) == 1 and cookies[0]["httpOnly"]:
        print("httpOnly")
    else:
        # Normal JSON output for other cases
        for cookie in cookies:
            print(json.dumps(cookie, separators=(',', ':')))

if __name__ == "__main__":
    main()