import hmac
import hashlib
import json
import sys
import time
import base64

# Secret key for HMAC (in a real app, this would be stored securely)
SECRET_KEY = b"csrf_secret_key_2023"

def generate_token(session_id):
    # Token expires in 1 hour (3600 seconds)
    expires_at = int(time.time()) + 3600
    
    # Create message to sign: session_id + expires_at
    message = f"{session_id}:{expires_at}".encode('utf-8')
    
    # Generate HMAC signature
    signature = hmac.new(SECRET_KEY, message, hashlib.sha256).digest()
    
    # Encode signature as base64
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    
    # Create token: base64(session_id:expires_at:signature)
    token_data = f"{session_id}:{expires_at}:{signature_b64}"
    token = base64.b64encode(token_data.encode('utf-8')).decode('utf-8')
    
    return {
        "token": token,
        "expiresAt": expires_at
    }

def validate_token(session_id, token):
    try:
        # Decode token
        token_data = base64.b64decode(token.encode('utf-8')).decode('utf-8')
        parts = token_data.split(':')
        
        if len(parts) != 3:
            return "INVALID: malformed token"
        
        token_session_id, expires_at_str, signature_b64 = parts
        
        # Check session ID matches
        if token_session_id != session_id:
            return "INVALID: session ID mismatch"
        
        expires_at = int(expires_at_str)
        
        # Check if token is expired
        if time.time() > expires_at:
            return "INVALID: token expired"
        
        # Verify signature
        message = f"{session_id}:{expires_at}".encode('utf-8')
        expected_signature = hmac.new(SECRET_KEY, message, hashlib.sha256).digest()
        provided_signature = base64.b64decode(signature_b64.encode('utf-8'))
        
        if not hmac.compare_digest(expected_signature, provided_signature):
            return "INVALID: signature verification failed"
        
        return "VALID"
        
    except Exception as e:
        return f"INVALID: {str(e)}"

def main():
    # Read command
    command = sys.stdin.readline().strip()
    
    # Read session ID
    session_id = sys.stdin.readline().strip()
    
    if command == "generate":
        result = generate_token(session_id)
        print(json.dumps(result))
    elif command == "validate":
        # Read token to validate
        token = sys.stdin.readline().strip()
        result = validate_token(session_id, token)
        print(result)
    else:
        print("INVALID: unknown command")

if __name__ == "__main__":
    main()