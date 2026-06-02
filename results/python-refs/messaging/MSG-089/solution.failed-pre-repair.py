import sys
import secrets
import hashlib
from datetime import datetime

def generate_ephemeral_key():
    """Generate a new ephemeral key"""
    return secrets.token_hex(32)

def derive_session_key(identity_key, ephemeral_key):
    """Derive a new session key from identity and ephemeral keys"""
    combined = identity_key + ephemeral_key
    return hashlib.sha256(combined.encode()).hexdigest()

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    old_session_key = lines[0]
    reason = lines[1]
    new_identity_key = lines[2]
    pending_count = int(lines[3])
    
    # Generate new ephemeral key
    new_ephemeral_key = generate_ephemeral_key()
    
    # Derive new session key
    new_session_key = derive_session_key(new_identity_key, new_ephemeral_key)
    
    # Get current timestamp
    established_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Print renegotiation protocol steps
    print("RENEGOTIATION:")
    print(f"1. Suspend message delivery ({pending_count} pending)")
    print("2. Generate new ephemeral key")
    print("3. Send renegotiation request")
    print("4. Await acknowledgement")
    print("5. Derive new session key")
    print(f"6. Re-encrypt {pending_count} pending messages")
    print("7. Resume delivery")
    print(f"new_session: {{{new_session_key}, {established_at}}}")

if __name__ == "__main__":
    main()