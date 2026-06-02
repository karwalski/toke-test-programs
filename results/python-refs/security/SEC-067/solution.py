import sys
import math
from collections import Counter

def calculate_entropy(key):
    if not key:
        return 0
    
    # Count frequency of each character
    char_counts = Counter(key)
    key_length = len(key)
    
    # Calculate Shannon entropy
    entropy = 0
    for count in char_counts.values():
        probability = count / key_length
        if probability > 0:
            entropy -= probability * math.log2(probability)
    
    # Return entropy in bits
    return entropy * key_length

def analyze_charset(key):
    has_lower = any(c.islower() for c in key)
    has_upper = any(c.isupper() for c in key)
    has_digit = any(c.isdigit() for c in key)
    has_special = any(not c.isalnum() for c in key)
    
    charset_parts = []
    if has_lower:
        charset_parts.append("lowercase")
    if has_upper:
        charset_parts.append("uppercase")
    if has_digit:
        charset_parts.append("digits")
    if has_special:
        charset_parts.append("special")
    
    return "+".join(charset_parts) if charset_parts else "unknown"

def check_predictability(key):
    issues = []
    
    # Check for common patterns
    if key.lower().startswith(('key-', 'api-', 'secret-', 'token-')):
        issues.append("common_prefix")
    
    # Check for sequential characters
    sequential_count = 0
    for i in range(len(key) - 2):
        if ord(key[i+1]) == ord(key[i]) + 1 and ord(key[i+2]) == ord(key[i+1]) + 1:
            sequential_count += 1
    if sequential_count > 0:
        issues.append("sequential_chars")
    
    # Check for repeated patterns
    for i in range(2, len(key) // 2 + 1):
        pattern = key[:i]
        if key.startswith(pattern * (len(key) // i)):
            issues.append("repeated_pattern")
            break
    
    # Check for common weak patterns
    if key.isdigit():
        issues.append("digits_only")
    elif key.isalpha():
        issues.append("letters_only")
    elif len(set(key)) < len(key) * 0.5:
        issues.append("low_character_variety")
    
    return issues

def determine_strength(key, entropy_bits, issues):
    # Base strength on entropy and length
    if len(key) < 16:
        return "weak"
    elif entropy_bits < 32:
        return "weak"
    elif len(issues) > 2:
        return "weak"
    elif entropy_bits < 64 or len(issues) > 0:
        return "fair"
    else:
        return "strong"

def analyze_api_key(key):
    key = key.strip()
    if not key:
        return None
    
    prefix = key[:4]
    length = len(key)
    entropy_bits = calculate_entropy(key)
    charset = analyze_charset(key)
    issues = check_predictability(key)
    strength = determine_strength(key, entropy_bits, issues)
    
    return {
        'prefix': prefix,
        'length': length,
        'entropy_bits': entropy_bits,
        'charset': charset,
        'strength': strength,
        'issues': issues
    }

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        result = analyze_api_key(line)
        if result:
            print(result['strength'])

if __name__ == "__main__":
    main()