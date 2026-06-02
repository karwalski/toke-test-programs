import sys

def analyze_cipher_suite(cipher_name):
    cipher_name = cipher_name.strip().upper()
    
    # Define patterns for insecure components
    insecure_patterns = [
        'RC4', 'DES', 'NULL', 'EXPORT', 'MD5', 'SHA1', 'ADH', 'AECDH'
    ]
    
    # Define patterns for weak components
    weak_patterns = [
        'RSA_WITH_', '3DES', 'CBC'
    ]
    
    # Define patterns for acceptable/strong components
    strong_patterns = [
        'ECDHE', 'DHE', 'AES_256_GCM', 'AES_128_GCM', 'CHACHA20_POLY1305'
    ]
    
    acceptable_patterns = [
        'AES_256', 'AES_128'
    ]
    
    issues = []
    strength = "acceptable"
    
    # Check for insecure patterns
    for pattern in insecure_patterns:
        if pattern in cipher_name:
            if pattern == 'RC4':
                issues.append("RC4 cipher is broken")
            elif pattern == 'NULL':
                issues.append("No encryption")
            elif pattern == 'EXPORT':
                issues.append("Export-grade encryption")
            elif pattern == 'MD5':
                issues.append("MD5 is cryptographically broken")
            elif pattern in ['ADH', 'AECDH']:
                issues.append("Anonymous key exchange")
            strength = "insecure"
    
    # Check for weak patterns if not already insecure
    if strength != "insecure":
        for pattern in weak_patterns:
            if pattern in cipher_name:
                if pattern == 'RSA_WITH_':
                    issues.append("No forward secrecy")
                elif pattern == '3DES':
                    issues.append("3DES is deprecated")
                elif pattern == 'CBC':
                    issues.append("CBC mode vulnerable to attacks")
                if strength != "weak":
                    strength = "weak"
    
    # Check for strong patterns
    if strength == "acceptable":
        has_strong = any(pattern in cipher_name for pattern in strong_patterns)
        if has_strong:
            strength = "strong"
    
    # Generate recommendation
    if strength == "insecure":
        recommendation = "Replace with TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 or TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256"
    elif strength == "weak":
        recommendation = "Upgrade to ECDHE with AEAD cipher"
    elif strength == "acceptable":
        recommendation = "Consider upgrading to ECDHE for forward secrecy"
    else:  # strong
        recommendation = "Good modern cipher suite"
    
    return {
        'name': cipher_name,
        'strength': strength,
        'issues': issues,
        'recommendation': recommendation
    }

def main():
    for line in sys.stdin:
        cipher_name = line.strip()
        if cipher_name:
            result = analyze_cipher_suite(cipher_name)
            print(result['strength'])

if __name__ == "__main__":
    main()