import json
import sys
import secrets
import base64

def generate_totp_secret():
    """Generate a random 160-bit TOTP secret and encode it as base32"""
    # Generate 20 random bytes (160 bits)
    secret_bytes = secrets.token_bytes(20)
    # Encode as base32 (RFC 3548)
    secret_b32 = base64.b32encode(secret_bytes).decode('ascii')
    # Remove padding
    return secret_b32.rstrip('=')

def create_provisioning_uri(secret, issuer="SocialApp", account="alice"):
    """Create TOTP provisioning URI"""
    return f"otpauth://totp/{issuer}:{account}?secret={secret}"

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Check if this is a 2FA setup request
    if input_data.get("action") == "setup_2fa":
        # Generate TOTP secret
        secret = generate_totp_secret()
        
        # Create provisioning URI
        provisioning_uri = create_provisioning_uri(secret)
        
        # Create response
        response = {
            "secret": secret,
            "provisioning_uri": provisioning_uri,
            "status": "pending_verification"
        }
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))
    else:
        # Handle other actions if needed
        response = {"error": "Unknown action"}
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()