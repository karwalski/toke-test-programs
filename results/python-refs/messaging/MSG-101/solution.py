import sys
import hashlib
import hmac
import secrets

def hkdf_extract(salt, ikm):
    if salt is None or len(salt) == 0:
        salt = b'\x00' * 48  # SHA384 hash length
    return hmac.new(salt, ikm, hashlib.sha384).digest()

def hkdf_expand(prk, info, length):
    t = b''
    okm = b''
    counter = 1
    
    while len(okm) < length:
        t = hmac.new(prk, t + info + bytes([counter]), hashlib.sha384).digest()
        okm += t
        counter += 1
    
    return okm[:length]

def derive_secret(secret, label, messages):
    transcript_hash = hashlib.sha384(messages).digest()
    hkdf_label = (
        (len(label) + 6).to_bytes(2, 'big') +  # length of "tls13 " + label
        b'tls13 ' + label.encode() +
        len(transcript_hash).to_bytes(1, 'big') +
        transcript_hash
    )
    return hkdf_expand(secret, hkdf_label, 48)

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    client_ciphers = lines[0].split(',')
    server_cert = lines[1]
    client_key_share = lines[2]
    
    # Simulate handshake
    print(f"1. ClientHello (ciphers: {len(client_ciphers)}, key_share: x25519)")
    
    # Server selects first cipher
    selected_cipher = client_ciphers[0]
    print(f"2. ServerHello (selected: {selected_cipher})")
    
    print("3. Server Certificate")
    print("4. Server CertificateVerify")
    
    # Generate some fake secrets for demonstration
    shared_secret = secrets.token_bytes(32)
    
    # Simulate message transcript
    client_hello = b"ClientHello_" + ','.join(client_ciphers).encode()
    server_hello = b"ServerHello_" + selected_cipher.encode()
    certificate = b"Certificate_" + server_cert.encode()
    cert_verify = b"CertificateVerify"
    
    messages_so_far = client_hello + server_hello + certificate + cert_verify
    
    # Derive handshake secret
    early_secret = hkdf_extract(None, b'')
    handshake_secret = hkdf_extract(derive_secret(early_secret, "derived", b''), shared_secret)
    
    # Derive finished keys
    server_finished_key = derive_secret(handshake_secret, "s hs traffic", messages_so_far)
    
    # Server finished
    server_verify_data = hmac.new(server_finished_key[:32], 
                                  hashlib.sha384(messages_so_far).digest(), 
                                  hashlib.sha384).digest()[:12]
    
    print(f"5. Server Finished (verify_data: {server_verify_data.hex()})")
    
    # Add server finished to transcript
    messages_so_far += b"Finished_" + server_verify_data
    
    # Client finished
    client_finished_key = derive_secret(handshake_secret, "c hs traffic", messages_so_far)
    client_verify_data = hmac.new(client_finished_key[:32], 
                                  hashlib.sha384(messages_so_far).digest(), 
                                  hashlib.sha384).digest()[:12]
    
    print(f"6. Client Finished (verify_data: {client_verify_data.hex()})")
    
    # Derive master secret
    messages_so_far += b"Finished_" + client_verify_data
    master_secret = hkdf_extract(derive_secret(handshake_secret, "derived", messages_so_far), b'\x00' * 48)
    
    print(f"handshake_secret: {handshake_secret.hex()}")
    print(f"master_secret: {master_secret.hex()}")

if __name__ == "__main__":
    main()