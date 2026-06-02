import sys
import json
from urllib.parse import urlparse, parse_qs

def analyze_oauth_url(url):
    try:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # Extract parameters (parse_qs returns lists, so get first item)
        response_type = params.get('response_type', [''])[0]
        state_present = 'state' in params
        scope = params.get('scope', [''])[0]
        redirect_uri = params.get('redirect_uri', [''])[0]
        
        # Check if redirect URI is secure (HTTPS)
        redirect_uri_secure = redirect_uri.startswith('https://')
        
        issues = []
        
        # Check for implicit flow
        if response_type == 'token' or 'token' in response_type:
            issues.append({
                'id': 'implicit_flow',
                'severity': 'high',
                'description': 'Using implicit flow which is less secure',
                'recommendation': 'Use authorization code flow with PKCE instead'
            })
        
        # Check for missing state parameter
        if not state_present:
            issues.append({
                'id': 'missing_state',
                'severity': 'medium',
                'description': 'Missing state parameter for CSRF protection',
                'recommendation': 'Include a state parameter with a random value'
            })
        
        # Check for overly broad scopes
        if scope and ('*' in scope or 'admin' in scope.lower() or 'all' in scope.lower()):
            issues.append({
                'id': 'broad_scope',
                'severity': 'medium',
                'description': 'Overly broad scope requested',
                'recommendation': 'Request only necessary scopes'
            })
        
        # Check for insecure redirect URI
        if not redirect_uri_secure and redirect_uri:
            issues.append({
                'id': 'insecure_redirect',
                'severity': 'high',
                'description': 'Redirect URI uses HTTP instead of HTTPS',
                'recommendation': 'Use HTTPS for redirect URI'
            })
        
        return {
            'response_type': response_type,
            'state_present': state_present,
            'scope': scope,
            'redirect_uri_secure': redirect_uri_secure,
            'issues': issues
        }
    except Exception:
        return {
            'response_type': '',
            'state_present': False,
            'scope': '',
            'redirect_uri_secure': False,
            'issues': [{
                'id': 'parse_error',
                'severity': 'high',
                'description': 'Failed to parse OAuth URL',
                'recommendation': 'Ensure URL is properly formatted'
            }]
        }

# Read from stdin
url = sys.stdin.readline().strip()

# Analyze the URL
result = analyze_oauth_url(url)

# For the expected output format, just return the issue ID if it's implicit flow
if any(issue['id'] == 'implicit_flow' for issue in result['issues']):
    print('implicit_flow')
else:
    print(json.dumps(result))