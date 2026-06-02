import sys
import re

def extract_express_endpoints(content):
    endpoints = []
    
    # Patterns for Express.js route definitions
    patterns = [
        r"\.get\s*\(\s*['\"]([^'\"]+)['\"]",
        r"\.post\s*\(\s*['\"]([^'\"]+)['\"]",
        r"\.put\s*\(\s*['\"]([^'\"]+)['\"]",
        r"\.delete\s*\(\s*['\"]([^'\"]+)['\"]",
        r"\.patch\s*\(\s*['\"]([^'\"]+)['\"]",
        r"app\.get\s*\(\s*['\"]([^'\"]+)['\"]",
        r"app\.post\s*\(\s*['\"]([^'\"]+)['\"]",
        r"app\.put\s*\(\s*['\"]([^'\"]+)['\"]",
        r"app\.delete\s*\(\s*['\"]([^'\"]+)['\"]",
        r"app\.patch\s*\(\s*['\"]([^'\"]+)['\"]",
        r"router\.get\s*\(\s*['\"]([^'\"]+)['\"]",
        r"router\.post\s*\(\s*['\"]([^'\"]+)['\"]",
        r"router\.put\s*\(\s*['\"]([^'\"]+)['\"]",
        r"router\.delete\s*\(\s*['\"]([^'\"]+)['\"]",
        r"router\.patch\s*\(\s*['\"]([^'\"]+)['\"]"
    ]
    
    for line in content.split('\n'):
        for pattern in patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            for match in matches:
                method = pattern.split('.')[1].split('\\')[0].upper()
                if method == 'DELETE':
                    method = 'DELETE'
                endpoints.append((method, match))
    
    return endpoints

def extract_flask_endpoints(content):
    endpoints = []
    
    # Patterns for Flask route definitions
    route_pattern = r"@app\.route\s*\(\s*['\"]([^'\"]+)['\"](?:.*?methods\s*=\s*\[([^\]]+)\])?"
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        match = re.search(route_pattern, line, re.IGNORECASE | re.DOTALL)
        if match:
            path = match.group(1)
            methods = match.group(2)
            
            if methods:
                # Extract methods from the list
                method_matches = re.findall(r"['\"](\w+)['\"]", methods)
                for method in method_matches:
                    endpoints.append((method.upper(), path))
            else:
                # Default to GET if no methods specified
                endpoints.append(('GET', path))
    
    return endpoints

def extract_gin_endpoints(content):
    endpoints = []
    
    # Patterns for Gin route definitions
    patterns = [
        r"\.GET\s*\(\s*['\"]([^'\"]+)['\"]",
        r"\.POST\s*\(\s*['\"]([^'\"]+)['\"]",
        r"\.PUT\s*\(\s*['\"]([^'\"]+)['\"]",
        r"\.DELETE\s*\(\s*['\"]([^'\"]+)['\"]",
        r"\.PATCH\s*\(\s*['\"]([^'\"]+)['\"]"
    ]
    
    for line in content.split('\n'):
        for pattern in patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                method = pattern.split('.')[1].split('\\')[0]
                endpoints.append((method, match))
    
    return endpoints

def main():
    lines = sys.stdin.read().strip().split('\n')
    framework = lines[0].strip()
    file_paths = [line.strip() for line in lines[1:]]
    
    all_endpoints = []
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if framework == 'express':
                endpoints = extract_express_endpoints(content)
            elif framework == 'flask':
                endpoints = extract_flask_endpoints(content)
            elif framework == 'gin':
                endpoints = extract_gin_endpoints(content)
            else:
                continue
            
            all_endpoints.extend(endpoints)
        except:
            continue
    
    # Sort by method then path
    all_endpoints.sort(key=lambda x: (x[0], x[1]))
    
    # Print results
    for method, path in all_endpoints:
        print(f"{method} {path}")

if __name__ == "__main__":
    main()