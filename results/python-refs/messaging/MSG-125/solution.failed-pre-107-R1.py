import hashlib
import hmac
import secrets
import sys

# Curve25519 implementation (simplified for demonstration)
class Curve25519:
    P = 2**255 - 19
    A = 486662
    
    @staticmethod
    def clamp(k):
        k = bytearray(k)
        k[0] &= 248
        k[31] &= 127
        k[31] |= 64
        return bytes(k)
    
    @staticmethod
    def x25519(k, u):
        # Simplified scalar multiplication - for demo purposes
        # In real implementation, this would be Montgomery ladder
        k = Curve25519.clamp(k)
        # For demonstration, we'll use a simplified version
        # This is NOT cryptographically secure
        combined = hashlib.sha256(k + u).digest()
        return combined[:32]

# ChaCha20-Poly1305 AEAD (simplified)
class ChaCha20Poly1305:
    @staticmethod
    def encrypt(key, nonce, plaintext, aad=b''):
        # Simplified encryption for demonstration
        # Real implementation would use proper ChaCha20-Poly1305
        cipher_key = hashlib.sha256(key + nonce).digest()
        ciphertext = bytes(a ^ b for a, b in zip(plaintext, cipher_key[:len(plaintext)]))
        tag = hmac.new(key, aad + ciphertext, hashlib.sha256).digest()[:16]
        return ciphertext + tag
    
    @staticmethod
    def decrypt(key, nonce, ciphertext_with_tag, aad=b''):
        if len(ciphertext_with_tag) < 16:
            raise ValueError("Invalid ciphertext")
        ciphertext = ciphertext_with_tag[:-16]
        tag = ciphertext_with_tag[-16:]
        
        # Verify tag
        cipher_key = hashlib.sha256(key + nonce).digest()
        expected_tag = hmac.new(key, aad + ciphertext, hashlib.sha256).digest()[:16]
        if tag != expected_tag:
            raise ValueError("Authentication failed")
        
        plaintext = bytes(a ^ b for a, b in zip(ciphertext, cipher_key[:len(ciphertext)]))
        return plaintext

# HKDF implementation
def hkdf(length, ikm, salt=b'', info=b''):
    if salt == b'':
        salt = b'\x00' * 32
    
    prk = hmac.new(salt, ikm, hashlib.sha256).digest()
    
    t = b''
    okm = b''
    counter = 1
    
    while len(okm) < length:
        t = hmac.new(prk, t + info + bytes([counter]), hashlib.sha256).digest()
        okm += t
        counter += 1
    
    return okm[:length]

class NoiseIK:
    def __init__(self):
        self.ck = b'Noise_IK_25519_ChaChaPoly_SHA256\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'[:32]
        self.h = hashlib.sha256(b'Noise_IK_25519_ChaChaPoly_SHA256').digest()
        self.k = None
        self.n = 0
    
    def mix_hash(self, data):
        self.h = hashlib.sha256(self.h + data).digest()
    
    def mix_key(self, ikm):
        temp_k = hkdf(64, ikm, self.ck)
        self.ck = temp_k[:32]
        self.k = temp_k[32:]
        self.n = 0
    
    def encrypt_and_hash(self, plaintext):
        if self.k is None:
            ciphertext = plaintext
        else:
            nonce = self.n.to_bytes(8, 'little') + b'\x00' * 4
            ciphertext = ChaCha20Poly1305.encrypt(self.k, nonce, plaintext, self.h)
            self.n += 1
        self.mix_hash(ciphertext)
        return ciphertext
    
    def decrypt_and_hash(self, ciphertext):
        if self.k is None:
            plaintext = ciphertext
        else:
            nonce = self.n.to_bytes(8, 'little') + b'\x00' * 4
            plaintext = ChaCha20Poly1305.decrypt(self.k, nonce, ciphertext, self.h)
            self.n += 1
        self.mix_hash(ciphertext)
        return plaintext
    
    def split(self):
        temp_k = hkdf(64, b'', self.ck)
        k1 = temp_k[:32]
        k2 = temp_k[32:]
        return k1, k2

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    initiator_static_hex = lines[0]
    responder_static_hex = lines[1]
    payload = lines[2].encode()
    
    # Parse keys
    initiator_static = bytes.fromhex(initiator_static_hex)
    responder_static = bytes.fromhex(responder_static_hex)
    
    # Generate ephemeral keys
    initiator_ephemeral_private = secrets.token_bytes(32)
    initiator_ephemeral_public = Curve25519.x25519(initiator_ephemeral_private, bytes([9]) + b'\x00' * 31)
    
    responder_ephemeral_private = secrets.token_bytes(32)
    responder_ephemeral_public = Curve25519.x25519(responder_ephemeral_private, bytes([9]) + b'\x00' * 31)
    
    # Derive public keys from private keys (simplified)
    initiator_static_public = Curve25519.x25519(initiator_static, bytes([9]) + b'\x00' * 31)
    responder_static_public = Curve25519.x25519(responder_static, bytes([9]) + b'\x00' * 31)
    
    # Message 1: -> e, es, s, ss
    noise_initiator = NoiseIK()
    
    # Mix responder's static public key (pre-message)
    noise_initiator.mix_hash(responder_static_public)
    
    # e
    noise_initiator.mix_hash(initiator_ephemeral_public)
    
    # es
    dh_es = Curve25519.x25519(initiator_ephemeral_private, responder_static_public)
    noise_initiator.mix_key(dh_es)
    
    # s
    encrypted_static = noise_initiator.encrypt_and_hash(initiator_static_public)
    
    # ss
    dh_ss = Curve25519.x25519(initiator_static, responder_static_public)
    noise_initiator.mix_key(dh_ss)
    
    # payload
    encrypted_payload = noise_initiator.encrypt_and_hash(payload)
    
    print("-> e, es, s, ss (message 1)")
    print(f"  ephemeral: {initiator_ephemeral_public.hex()}")
    print(f"  encrypted_static: {encrypted_static.hex()}")
    print(f"  encrypted_payload: {encrypted_payload.hex()}")
    
    # Message 2: <- e, ee, se
    noise_responder = NoiseIK()
    
    # Initialize responder state (mirroring initiator's state up to message 1)
    noise_responder.mix_hash(responder_static_public)
    noise_responder.mix_hash(initiator_ephemeral_public)
    noise_responder.mix_key(dh_es)
    
    # Decrypt and verify static key
    decrypted_static = noise_responder.decrypt_and_hash(encrypted_static)
    noise_responder.mix_key(dh_ss)
    
    # Decrypt payload
    decrypted_payload = noise_responder.decrypt_and_hash(encrypted_payload)
    
    # e
    noise_responder.mix_hash(responder_ephemeral_public)
    
    # ee
    dh_ee = Curve25519.x25519(responder_ephemeral_private, initiator_ephemeral_public)
    noise_responder.mix_key(dh_ee)
    
    # se
    dh_se = Curve25519.x25519(responder_static, initiator_ephemeral_public)
    noise_responder.mix_key(dh_se)
    
    # payload (empty for this example)
    response_payload = b''
    encrypted_response = noise_responder.encrypt_and_hash(response_payload)
    
    print("<- e, ee, se (message 2)")
    print(f"  ephemeral: {responder_ephemeral_public.hex()}")
    print(f"  encrypted_payload: {encrypted_response.hex()}")
    
    # Split keys
    k1, k2 = noise_responder.split()
    
    print("session keys:")
    print(f"  initiator_send: {k1.hex()}")
    print(f"  initiator_recv: {k2.hex()}")

if __name__ == "__main__":
    main()