import sys
import urllib.request
import urllib.parse
import json

def test_hpp_vulnerability(url):
    # Parse the URL
    parsed_url = urllib.parse.urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    
    # Get existing query parameters
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    # Choose a test parameter - use existing one if available, otherwise create new
    if query_params:
        test_param = list(query_params.keys())[0]
    else:
        test_param = 'test'
    
    # Test values
    test_values = ['first_value', 'second_value']
    
    try:
        # Create URL with duplicate parameters
        test_query = f"{test_param}={test_values[0]}&{test_param}={test_values[1]}"
        if parsed_url.query and test_param not in query_params:
            test_url = f"{base_url}?{parsed_url.query}&{test_query}"
        else:
            test_url = f"{base_url}?{test_query}"
        
        # Send request
        request = urllib.request.Request(test_url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        with urllib.request.urlopen(request, timeout=10) as response:
            response_text = response.read().decode('utf-8', errors='ignore')
            
        # Analyze server behavior
        first_in_response = test_values[0] in response_text
        second_in_response = test_values[1] in response_text
        
        if first_in_response and second_in_response:
            server_behaviour = "all"
            vulnerable = True
            potential_impact = "Parameter pollution may allow bypassing input validation or filters"
        elif first_in_response and not second_in_response:
            server_behaviour = "first"
            vulnerable = True
            potential_impact = "Server uses first parameter value, may bypass validation expecting last value"
        elif not first_in_response and second_in_response:
            server_behaviour = "last"
            vulnerable = True
            potential_impact = "Server uses last parameter value, may bypass validation expecting first value"
        else:
            server_behaviour = "first"  # Default assumption
            vulnerable = False
            potential_impact = "Low risk - standard parameter handling detected"
            
    except Exception:
        server_behaviour = "error"
        vulnerable = False
        potential_impact = "Unable to determine due to connection error"
    
    return {
        "parameter": test_param,
        "test_values": test_values,
        "server_behaviour": server_behaviour,
        "vulnerable": vulnerable,
        "potential_impact": potential_impact
    }

# Read URL from stdin
url = input().strip()

# Test for HPP vulnerability
result = test_hpp_vulnerability(url)

# Output only the server_behaviour as requested
print(result["server_behaviour"])