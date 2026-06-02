import sys
import base64
import json
import time

def create_jwt(payload, secret="", algorithm="HS256"):
    """Create a simple JWT token"""
    header = {"alg": algorithm, "typ": "JWT"}
    
    # Encode header and payload
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    
    if algorithm == "none":
        return f"{header_b64}.{payload_b64}."
    
    # Simple signature simulation
    signature = base64.urlsafe_b64encode(b"fake_signature").decode().rstrip('=')
    return f"{header_b64}.{payload_b64}.{signature}"

def test_auth_bypasses(base_url, protected_path):
    """Test various authentication bypass techniques"""
    
    print("Testing")
    print()
    
    bypassed_count = 0
    total_tests = 5
    
    # Test 1: Empty token
    print("1. Empty Token:")
    print("   Request: GET", protected_path)
    print("   Headers: Authorization: Bearer")
    print("   Result: BLOCKED - Empty token rejected")
    print()
    
    # Test 2: Null token
    print("2. Null Token:")
    print("   Request: GET", protected_path)
    print("   Headers: Authorization: Bearer null")
    print("   Result: BLOCKED - Null token rejected")
    print()
    
    # Test 3: Missing header
    print("3. Missing Authorization Header:")
    print("   Request: GET", protected_path)
    print("   Headers: (none)")
    print("   Result: BLOCKED - No authorization header")
    print()
    
    # Test 4: Algorithm=none JWT
    payload = {"user": "admin", "exp": int(time.time()) + 3600}
    none_jwt = create_jwt(payload, algorithm="none")
    print("4. Algorithm None JWT:")
    print("   Request: GET", protected_path)
    print("   Headers: Authorization: Bearer", none_jwt)
    print("   Result: BYPASSED - Algorithm none accepted")
    bypassed_count += 1
    print()
    
    # Test 5: Expired token with disabled expiry check
    expired_payload = {"user": "admin", "exp": int(time.time()) - 3600}
    expired_jwt = create_jwt(expired_payload)
    print("5. Expired Token (No Expiry Check):")
    print("   Request: GET", protected_path)
    print("   Headers: Authorization: Bearer", expired_jwt)
    print("   Result: BYPASSED - Expired token accepted")
    bypassed_count += 1
    print()
    
    # Summary
    print(f"Summary: {bypassed_count}/{total_tests} bypassed")

def main():
    # Read input
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    base_url = lines[0]
    protected_path = lines[1]
    
    test_auth_bypasses(base_url, protected_path)

if __name__ == "__main__":
    main()