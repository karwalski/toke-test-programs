import json
import sys
import re
import os

def scan_file(filepath, language):
    results = []
    
    if not os.path.exists(filepath):
        return results
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return results
    
    # Define vulnerability patterns based on language
    patterns = {
        'python': [
            (r'password\s*=\s*["\'][^"\']+["\']', 'HIGH', 'HARDCODED_PASSWORD', 'Hardcoded password detected'),
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'HIGH', 'HARDCODED_API_KEY', 'Hardcoded API key detected'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'HIGH', 'HARDCODED_SECRET', 'Hardcoded secret detected'),
            (r'eval\s*\(', 'HIGH', 'INSECURE_EVAL', 'Use of eval() function'),
            (r'exec\s*\(', 'HIGH', 'INSECURE_EXEC', 'Use of exec() function'),
            (r'input\s*\([^)]*\)', 'MEDIUM', 'INPUT_VALIDATION', 'Missing input validation'),
            (r'pickle\.loads?\s*\(', 'HIGH', 'INSECURE_DESERIALIZATION', 'Insecure pickle deserialization'),
            (r'TODO.*security', 'MEDIUM', 'TODO_SECURITY', 'Security TODO item'),
            (r'TODO.*SEC', 'MEDIUM', 'TODO_SECURITY', 'Security TODO item'),
        ],
        'javascript': [
            (r'password\s*[:=]\s*["\'][^"\']+["\']', 'HIGH', 'HARDCODED_PASSWORD', 'Hardcoded password detected'),
            (r'apiKey\s*[:=]\s*["\'][^"\']+["\']', 'HIGH', 'HARDCODED_API_KEY', 'Hardcoded API key detected'),
            (r'secret\s*[:=]\s*["\'][^"\']+["\']', 'HIGH', 'HARDCODED_SECRET', 'Hardcoded secret detected'),
            (r'eval\s*\(', 'HIGH', 'INSECURE_EVAL', 'Use of eval() function'),
            (r'innerHTML\s*=', 'MEDIUM', 'XSS_RISK', 'Potential XSS vulnerability'),
            (r'document\.write\s*\(', 'MEDIUM', 'XSS_RISK', 'Potential XSS vulnerability'),
            (r'TODO.*security', 'MEDIUM', 'TODO_SECURITY', 'Security TODO item'),
        ],
        'java': [
            (r'password\s*=\s*"[^"]+"', 'HIGH', 'HARDCODED_PASSWORD', 'Hardcoded password detected'),
            (r'apiKey\s*=\s*"[^"]+"', 'HIGH', 'HARDCODED_API_KEY', 'Hardcoded API key detected'),
            (r'Runtime\.getRuntime\(\)\.exec', 'HIGH', 'COMMAND_INJECTION', 'Command injection risk'),
            (r'TODO.*security', 'MEDIUM', 'TODO_SECURITY', 'Security TODO item'),
        ],
        'go': [
            (r'password\s*:?=\s*"[^"]+"', 'HIGH', 'HARDCODED_PASSWORD', 'Hardcoded password detected'),
            (r'apiKey\s*:?=\s*"[^"]+"', 'HIGH', 'HARDCODED_API_KEY', 'Hardcoded API key detected'),
            (r'exec\.Command\s*\(', 'MEDIUM', 'COMMAND_INJECTION', 'Command injection risk'),
            (r'TODO.*security', 'MEDIUM', 'TODO_SECURITY', 'Security TODO item'),
        ]
    }
    
    # Use patterns for specified language, or combine all for 'any'
    if language in patterns:
        selected_patterns = patterns[language]
    elif language == 'any':
        selected_patterns = []
        for lang_patterns in patterns.values():
            selected_patterns.extend(lang_patterns)
    else:
        selected_patterns = []
    
    # Scan each line
    for line_num, line in enumerate(lines, 1):
        for pattern, severity, rule_id, description in selected_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                col = match.start() + 1
                snippet = line.strip()
                if len(snippet) > 50:
                    snippet = snippet[:47] + "..."
                
                result = {
                    "line": line_num,
                    "col": col,
                    "severity": severity,
                    "rule_id": rule_id,
                    "description": description,
                    "snippet": snippet
                }
                results.append(result)
    
    return results

def main():
    # Read input
    filepath = input().strip()
    language = input().strip()
    
    # Scan file
    results = scan_file(filepath, language)
    
    # Output JSON
    print(json.dumps(results))

if __name__ == "__main__":
    main()