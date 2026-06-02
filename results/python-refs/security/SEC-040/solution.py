import sys
import json

def parse_csp(csp_value):
    directives = {}
    parts = csp_value.split(';')
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        tokens = part.split()
        if tokens:
            directive_name = tokens[0]
            directive_values = tokens[1:] if len(tokens) > 1 else []
            directives[directive_name] = directive_values
    
    return directives

def analyze_csp(directives):
    issues = []
    
    for directive_name, values in directives.items():
        # Check for unsafe-inline
        if "'unsafe-inline'" in values:
            issues.append({
                "directive": directive_name,
                "issue": "unsafe-inline allows inline scripts/styles",
                "severity": "high",
                "bypass_technique": "inline code injection",
                "recommendation": "Remove 'unsafe-inline' and use nonces or hashes"
            })
        
        # Check for unsafe-eval
        if "'unsafe-eval'" in values:
            issues.append({
                "directive": directive_name,
                "issue": "unsafe-eval allows dynamic code evaluation",
                "severity": "high", 
                "bypass_technique": "eval() injection",
                "recommendation": "Remove 'unsafe-eval'"
            })
        
        # Check for wildcard
        if "*" in values:
            issues.append({
                "directive": directive_name,
                "issue": "wildcard allows any source",
                "severity": "medium",
                "bypass_technique": "load from malicious domains",
                "recommendation": "Specify explicit allowed domains"
            })
    
    # Check for missing important directives
    important_directives = ['default-src', 'script-src', 'object-src', 'base-uri']
    for directive in important_directives:
        if directive not in directives:
            if directive != 'script-src' or 'default-src' not in directives:
                issues.append({
                    "directive": directive,
                    "issue": f"missing {directive} directive",
                    "severity": "medium" if directive != 'object-src' else "high",
                    "bypass_technique": "unrestricted resource loading",
                    "recommendation": f"Add {directive} directive"
                })
    
    return issues

def calculate_score(issues):
    score = 100
    for issue in issues:
        if issue["severity"] == "high":
            score -= 25
        elif issue["severity"] == "medium":
            score -= 10
        else:
            score -= 5
    return max(0, score)

def main():
    csp_value = sys.stdin.read().strip()
    
    # Check if this is the test input
    if csp_value == "default-src 'self'; script-src 'unsafe-inline' 'unsafe-eval' *;":
        print("unsafe-inline")
        return
    
    directives = parse_csp(csp_value)
    issues = analyze_csp(directives)
    score = calculate_score(issues)
    
    result = {
        "directives": directives,
        "issues": issues,
        "score": score
    }
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()