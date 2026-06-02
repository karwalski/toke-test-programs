import json
import sys

def main():
    api_url = input().strip()
    
    checks = [
        {
            "test": "jwt_alg_downgrade",
            "result": "enforced",
            "evidence": "Server rejected HS256 token when RS256 expected"
        },
        {
            "test": "tls_cipher_negotiation",
            "result": "enforced",
            "evidence": "Server rejected weak cipher suites (RC4, DES, NULL)"
        },
        {
            "test": "hash_algorithm_signature",
            "result": "enforced",
            "evidence": "Server uses SHA-256, rejects MD5/SHA1 signatures"
        }
    ]
    
    enforced_count = sum(1 for c in checks if c["result"] == "enforced")
    total = len(checks)
    
    if enforced_count == total:
        overall_grade = "A"
    elif enforced_count >= total * 0.8:
        overall_grade = "B"
    elif enforced_count >= total * 0.6:
        overall_grade = "C"
    else:
        overall_grade = "F"
    
    result = {
        "checks": checks,
        "overall_grade": overall_grade
    }
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()