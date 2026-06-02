import json
import sys

def get_algorithm_strength(category, algorithm):
    """Return (strength_bits, description) for an algorithm"""
    strengths = {
        'ciphers': {
            'AES-256-GCM': (256, '256-bit, AEAD'),
            'AES-256-CBC': (256, '256-bit'),
            'AES-128-GCM': (128, '128-bit, AEAD'),
            'AES-128-CBC': (128, '128-bit'),
            'ChaCha20': (256, '256-bit, stream'),
            '3DES': (112, '112-bit'),
            'DES': (56, '56-bit')
        },
        'key_exchange': {
            'X25519': (128, '128-bit equivalent'),
            'X448': (224, '224-bit equivalent'),
            'P-256': (128, '128-bit equivalent'),
            'P-384': (192, '192-bit equivalent'),
            'P-521': (256, '256-bit equivalent'),
            'RSA-2048': (112, '112-bit equivalent'),
            'RSA-3072': (128, '128-bit equivalent'),
            'RSA-4096': (152, '152-bit equivalent'),
            'DH-2048': (112, '112-bit equivalent')
        },
        'hash': {
            'SHA-256': (256, '256-bit'),
            'SHA-384': (384, '384-bit'),
            'SHA-512': (512, '512-bit'),
            'SHA-224': (224, '224-bit'),
            'SHA-1': (160, '160-bit'),
            'MD5': (128, '128-bit')
        }
    }
    return strengths.get(category, {}).get(algorithm, (0, 'unknown'))

def negotiate_algorithms(client_a, client_b):
    """Negotiate the strongest mutual algorithms"""
    negotiated = {}
    
    for category in ['ciphers', 'key_exchange', 'hash']:
        # Find common algorithms
        common = set(client_a[category]) & set(client_b[category])
        
        if not common:
            return None  # No compatible algorithms
        
        # Find the strongest common algorithm
        best_algo = None
        best_strength = -1
        
        for algo in common:
            strength, _ = get_algorithm_strength(category, algo)
            if strength > best_strength:
                best_strength = strength
                best_algo = algo
        
        negotiated[category] = best_algo
    
    return negotiated

def main():
    # Read input
    line1 = input().strip()
    line2 = input().strip()
    
    try:
        client_a = json.loads(line1)
        client_b = json.loads(line2)
    except json.JSONDecodeError:
        print("INCOMPATIBLE")
        return
    
    # Negotiate algorithms
    negotiated = negotiate_algorithms(client_a, client_b)
    
    if negotiated is None:
        print("INCOMPATIBLE")
        return
    
    # Get details for output
    cipher_strength, cipher_desc = get_algorithm_strength('ciphers', negotiated['ciphers'])
    kex_strength, kex_desc = get_algorithm_strength('key_exchange', negotiated['key_exchange'])
    hash_strength, hash_desc = get_algorithm_strength('hash', negotiated['hash'])
    
    # Overall strength is the minimum of all components
    overall_strength = min(cipher_strength, kex_strength, hash_strength)
    
    # Output in exact format
    print("negotiated:")
    print(f"  cipher: {negotiated['ciphers']} ({cipher_desc})")
    print(f"  key_exchange: {negotiated['key_exchange']} ({kex_desc})")
    print(f"  hash: {negotiated['hash']} ({hash_desc})")
    print(f"overall strength: {overall_strength}-bit equivalent")

if __name__ == "__main__":
    main()