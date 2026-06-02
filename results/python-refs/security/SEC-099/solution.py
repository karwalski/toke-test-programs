import sys
import json
import re
import math
from collections import Counter

def calculate_entropy(s):
    if not s:
        return 0
    counter = Counter(s)
    length = len(s)
    entropy = 0
    for count in counter.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    return entropy

def detect_likely_type(s, context_line):
    s_lower = s.lower()
    context_lower = context_line.lower()
    
    if any(keyword in context_lower for keyword in ['api_key', 'apikey', 'api-key']):
        return 'api_key'
    elif any(keyword in context_lower for keyword in ['password', 'passwd', 'pwd']):
        return 'password'
    elif any(keyword in context_lower for keyword in ['token', 'auth_token', 'access_token']):
        return 'token'
    elif any(keyword in context_lower for keyword in ['secret', 'secret_key']):
        return 'secret'
    elif any(keyword in context_lower for keyword in ['key']):
        return 'key'
    elif s.startswith(('sk-', 'pk-', 'rk-')):
        return 'api_key'
    elif len(s) >= 32 and all(c in '0123456789abcdefABCDEF' for c in s):
        return 'hex_key'
    else:
        return 'unknown'

def extract_strings(line):
    strings = []
    strings.extend(re.findall(r'"([^"]{8,})"', line))
    strings.extend(re.findall(r"'([^']{8,})'", line))
    strings.extend(re.findall(r'=\s*([A-Za-z0-9+/=_-]{8,})(?:\s|$|;|,)', line))
    return strings

def main():
    file_path = input().strip()
    entropy_threshold = float(input().strip())
    
    results = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except:
        print("[")
        return
    
    for line_num, line in enumerate(lines, 1):
        line = line.rstrip('\n\r')
        strings = extract_strings(line)
        
        for s in strings:
            entropy = calculate_entropy(s)
            if entropy >= entropy_threshold:
                likely_type = detect_likely_type(s, line)
                result = {
                    "line": line_num,
                    "entropy_bits": round(entropy, 2),
                    "string_prefix": s[:8],
                    "context_line": line,
                    "likely_type": likely_type
                }
                results.append(result)
    
    print("[")

if __name__ == "__main__":
    main()