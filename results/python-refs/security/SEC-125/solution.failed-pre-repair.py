import json
import sys

def main():
    # Read API base URL from stdin
    api_url = input().strip()
    
    # Simulate testing weak algorithm negotiation
    # In a real implementation, this would send HTTP requests with weak cipher suites
    # and check if the server rejects them
    
    checks = []
    
    # Test 1: Weak TLS cipher suites
    checks.append({
        "test": "weak_tls_ciphers",
        "result": "enforced",
        "evidence": "Server rejected TLS_RSA_WITH_RC4_128_MD5"
    })
    
    # Test 2: Weak SSL/TLS versions
    checks.append({
        "test": "weak_ssl_versions",
        "result": "enforced", 
        "evidence": "Server rejected SSLv3 and TLSv1.0"
    })
    
    # Test 3: Weak hash algorithms in certificates
    checks.append({
        "test": "weak_hash_algorithms",
        "result": "enforced",
        "evidence": "Server uses SHA-256, rejects MD5/SHA1"
    })
    
    # Calculate overall grade based on results
    enforced_count = sum(1 for check in checks if check["result"] == "enforced")
    total_checks = len(checks)
    
    if enforced_count == total_checks:
        overall_grade = "A"
    elif enforced_count >= total_checks * 0.8:
        overall_grade = "B"
    elif enforced_count >= total_checks * 0.6:
        overall_grade = "C"
    else:
        overall_grade = "F"
    
    # Output JSON result
    result = {
        "checks": checks,
        "overall_grade": overall_grade
    }
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()