import sys
import urllib.request
import urllib.parse
import json
import re
import time
import math
from collections import Counter

def calculate_entropy(token):
    """Calculate Shannon entropy of a token"""
    if not token:
        return 0
    
    # Count frequency of each character
    char_counts = Counter(token)
    length = len(token)
    
    # Calculate entropy
    entropy = 0
    for count in char_counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    
    return entropy

def test_entropy(token):
    """Test if token has sufficient entropy (> 4 bits per character)"""
    entropy = calculate_entropy(token)
    per_char_entropy = entropy
    return per_char_entropy > 4.0, f"Entropy: {per_char_entropy:.2f} bits/char"

def test_predictability(tokens):
    """Test if tokens show predictable patterns"""
    if len(tokens) < 2:
        return True, "Insufficient tokens for pattern analysis"
    
    # Check for sequential patterns
    for i in range(len(tokens) - 1):
        token1 = tokens[i]
        token2 = tokens[i + 1]
        
        # Simple check for incrementing patterns
        if token1.isdigit() and token2.isdigit():
            if int(token2) == int(token1) + 1:
                return False, "Sequential numeric pattern detected"
        
        # Check for similar structure
        if len(token1) == len(token2):
            diff_count = sum(1 for a, b in zip(token1, token2) if a != b)
            if diff_count <= 2:
                return False, "Similar token structure detected"
    
    return True, "No obvious patterns detected"

def make_request(url, data=None, method='GET'):
    """Make HTTP request and return response"""
    try:
        if data and method == 'POST':
            data = urllib.parse.urlencode(data).encode('utf-8')
            req = urllib.request.Request(url, data=data)
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        else:
            req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8'), response.code
    except Exception as e:
        return str(e), 0

def extract_token_from_response(response_text):
    """Extract reset token from response"""
    # Look for common token patterns
    patterns = [
        r'token["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_-]+)',
        r'reset["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_-]+)',
        r'/reset/([a-zA-Z0-9_-]+)',
        r'code["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response_text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def test_single_use(reset_url, token):
    """Test if token can only be used once"""
    if not token:
        return False, "No token available for testing"
    
    # Try to use the token twice
    test_url = f"{reset_url}?token={token}"
    
    response1, code1 = make_request(test_url)
    response2, code2 = make_request(test_url)
    
    if code1 == code2 and code1 == 200:
        return False, "Token accepted multiple times"
    
    return True, "Token appears to be single-use"

def test_expiry(reset_url, token):
    """Test if token has expiry enforcement"""
    if not token:
        return False, "No token available for testing"
    
    # This is a simplified test - in reality we'd wait or manipulate time
    test_url = f"{reset_url}?token={token}"
    response, code = make_request(test_url)
    
    # Look for expiry-related terms in response
    if any(term in response.lower() for term in ['expired', 'timeout', 'invalid']):
        return True, "Expiry enforcement detected"
    
    return False, "No clear expiry enforcement detected"

def main():
    # Read input
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    if len(lines) < 3:
        return
    
    forgot_url = lines[0]
    reset_url = lines[1]
    test_email = lines[2]
    
    print("Testing")

if __name__ == "__main__":
    main()