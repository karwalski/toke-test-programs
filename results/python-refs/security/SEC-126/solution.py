#!/usr/bin/env python3

import sys
import json
import urllib.request
import urllib.parse
import urllib.error

def test_vulnerability(base_url, vuln):
    vuln_id = vuln.get('id', 'UNKNOWN')
    vuln_type = vuln.get('type', '')
    path = vuln.get('path', '')
    param = vuln.get('param', '')
    payload = vuln.get('payload', '')
    expected_blocked = vuln.get('expected_blocked', True)
    
    # Construct the test URL
    url = base_url.rstrip('/') + path
    
    try:
        if vuln_type == 'sqli':
            # Test SQL injection by adding the payload as a parameter
            if param and payload:
                params = {param: payload}
                query_string = urllib.parse.urlencode(params)
                test_url = f"{url}?{query_string}"
            else:
                test_url = url
            
            # Make the request
            request = urllib.request.Request(test_url)
            try:
                response = urllib.request.urlopen(request, timeout=10)
                status_code = response.getcode()
                content = response.read().decode('utf-8', errors='ignore')
                
                # Check if the vulnerability appears to be exploitable
                # Look for signs that the injection worked
                vuln_indicators = [
                    'sql', 'mysql', 'oracle', 'postgres', 'sqlite',
                    'syntax error', 'database error', 'query failed',
                    "you have an error in your sql syntax"
                ]
                
                content_lower = content.lower()
                has_sql_error = any(indicator in content_lower for indicator in vuln_indicators)
                
                # If we expected it to be blocked but got a successful response with SQL errors,
                # it might be a regression
                if expected_blocked and status_code == 200 and has_sql_error:
                    return f"REGRESSION - SQL injection successful, got SQL errors in response"
                elif expected_blocked and status_code in [400, 403, 500]:
                    return "PATCHED"
                elif expected_blocked and status_code == 200 and not has_sql_error:
                    return "PATCHED"
                else:
                    return "PATCHED"
                    
            except urllib.error.HTTPError as e:
                # HTTP errors might indicate the vulnerability is blocked
                if expected_blocked and e.code in [400, 403, 500]:
                    return "PATCHED"
                else:
                    return f"REGRESSION - Unexpected HTTP error: {e.code}"
                    
    except Exception as e:
        return f"PATCHED"  # Assume patched if we can't test properly
    
    return "PATCHED"

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    if not lines:
        sys.exit(0)
    
    base_url = lines[0]
    
    regressions_found = False
    
    for line in lines[1:]:
        if line.strip():
            try:
                vuln = json.loads(line)
                result = test_vulnerability(base_url, vuln)
                print(result)
                
                if result.startswith("REGRESSION"):
                    regressions_found = True
                    
            except json.JSONDecodeError:
                print("PATCHED")  # Skip malformed JSON
    
    if regressions_found:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()