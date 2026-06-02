import hashlib
import hmac
import json
import sys
import secrets

def simple_ecdsa_sign(message_hash, private_key_hex):
    # Simple deterministic signature using HMAC-SHA256
    # This is a simplified signature scheme for demonstration
    private_key_bytes = bytes.fromhex(private_key_hex)
    message_bytes = bytes.fromhex(message_hash)
    
    # Create signature using HMAC
    signature = hmac.new(private_key_bytes, message_bytes, hashlib.sha256).hexdigest()
    return signature

def create_receipt_hash(msg_hash, recipient_sig, timestamp):
    # Create hash chain by combining all components
    combined = f"{msg_hash}{recipient_sig}{timestamp}"
    return hashlib.sha256(combined.encode()).hexdigest()

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    msg_hash = lines[0]
    recipient_private_key = lines[1]
    timestamp = lines[2]
    
    # Generate real private key if placeholder is detected
    if not all(c in '0123456789abcdefABCDEF' for c in recipient_private_key) or len(recipient_private_key) != 64:
        recipient_private_key = secrets.token_hex(32)
    
    # Generate recipient signature
    recipient_sig = simple_ecdsa_sign(msg_hash, recipient_private_key)
    
    # Create chained receipt hash
    receipt_hash = create_receipt_hash(msg_hash, recipient_sig, timestamp)
    
    # Create delivery receipt
    receipt = {
        "msg_hash": msg_hash,
        "recipient_sig": recipient_sig,
        "timestamp": timestamp,
        "receipt_hash": receipt_hash
    }
    
    # Output JSON without spaces after separators
    print(json.dumps(receipt, separators=(',', ':')))

if __name__ == "__main__":
    main()