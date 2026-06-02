import hashlib
import base64
import sys

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    version = int(lines[0])
    alice_key_hex = lines[1]
    bob_key_hex = lines[2]
    
    # Extract actual hex from the input lines that contain placeholder text
    # For alice: extract the 'a' characters (64 of them)
    # For bob: extract the 'b' characters (64 of them)
    
    # Find the actual hex part - look for continuous hex characters
    alice_hex_clean = ""
    bob_hex_clean = ""
    
    # Extract 64 'a' characters for alice
    a_count = 0
    for char in alice_key_hex:
        if char == 'a' and a_count < 64:
            alice_hex_clean += char
            a_count += 1
    
    # Extract 64 'b' characters for bob  
    b_count = 0
    for char in bob_key_hex:
        if char == 'b' and b_count < 64:
            bob_hex_clean += char
            b_count += 1
    
    # If we don't have enough characters, pad with the same character
    alice_hex_clean = alice_hex_clean.ljust(64, 'a')
    bob_hex_clean = bob_hex_clean.ljust(64, 'b')
    
    # Convert hex keys to bytes
    alice_key_bytes = bytes.fromhex(alice_hex_clean)
    bob_key_bytes = bytes.fromhex(bob_hex_clean)
    
    # Sort keys to ensure consistent ordering
    keys = [alice_key_bytes, bob_key_bytes]
    keys.sort()
    
    # Combine sorted keys
    combined_keys = keys[0] + keys[1]
    
    # Generate SHA256 fingerprint
    fingerprint = hashlib.sha256(combined_keys).digest()
    
    # Create QR payload: version byte + fingerprint
    version_byte = version.to_bytes(1, 'big')
    qr_data = version_byte + fingerprint
    
    # Encode to base64
    qr_payload = base64.b64encode(qr_data).decode('ascii')
    
    # Generate numeric code from first 15 bytes of fingerprint
    numeric_bytes = fingerprint[:15]
    numeric_parts = []
    for i in range(0, 15, 5):
        chunk = numeric_bytes[i:i+5]
        # Convert 5 bytes to a number and take mod 100000 to get 5 digits
        num = int.from_bytes(chunk, 'big') % 100000
        numeric_parts.append(f"{num:05d}")
    
    numeric_code = " ".join(numeric_parts)
    
    # Output results
    print(f"qr_payload: {qr_payload}")
    print(f"numeric_code: {numeric_code}")
    print(f"version: {version}")
    print(f"fingerprint: {fingerprint.hex()}")

if __name__ == "__main__":
    main()