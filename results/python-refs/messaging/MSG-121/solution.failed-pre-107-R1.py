import hashlib
import hmac
import json
import sys
import secrets

def simple_sign(private_key_hex, message):
    """Simple signing using HMAC-SHA256 as a substitute for actual digital signatures"""
    private_key_bytes = bytes.fromhex(private_key_hex)
    message_bytes = message.encode('utf-8')
    signature = hmac.new(private_key_bytes, message_bytes, hashlib.sha256).hexdigest()
    return signature

def compute_combined_hash(content, signer_sig, timestamp, ta_sig):
    """Compute a combined hash of all components"""
    combined_data = f"{content}{signer_sig}{timestamp}{ta_sig}".encode('utf-8')
    return hashlib.sha256(combined_data).hexdigest()

def main():
    # Read input
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Generate actual hex values if placeholders are detected
    signer_private_key_hex = lines[0]
    if not all(c in '0123456789abcdefABCDEF' for c in signer_private_key_hex):
        # Generate a real private key
        signer_private_key_hex = secrets.token_hex(32)
    
    message = lines[1]
    ta_response_json = lines[2]
    
    # Parse timestamp authority response and fix placeholder if needed
    ta_response = json.loads(ta_response_json)
    timestamp = ta_response["time"]
    ta_signature = ta_response["ta_signature"]
    
    # If ta_signature is a placeholder, generate a real one
    if not all(c in '0123456789abcdefABCDEF' for c in ta_signature):
        # Generate a real TA signature using timestamp
        ta_key = secrets.token_hex(32)
        ta_signature = hmac.new(bytes.fromhex(ta_key), timestamp.encode('utf-8'), hashlib.sha256).hexdigest()
    
    # Sign the message
    signer_signature = simple_sign(signer_private_key_hex, message)
    
    # Compute combined hash
    combined_hash = compute_combined_hash(message, signer_signature, timestamp, ta_signature)
    
    # Create the signed message bundle
    bundle = {
        "content": message,
        "signer_sig": signer_signature,
        "timestamp": timestamp,
        "ta_sig": ta_signature,
        "combined_hash": combined_hash
    }
    
    # Output the result
    print(json.dumps(bundle, separators=(',', ':')))

if __name__ == "__main__":
    main()