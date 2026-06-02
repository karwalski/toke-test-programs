import sys
import secrets
import base64
from math import gcd

def generate_prime(bits):
    """Generate a prime number with the specified number of bits."""
    while True:
        # Generate a random odd number with the right bit length
        n = secrets.randbits(bits)
        n |= (1 << bits - 1) | 1  # Set MSB and LSB to ensure odd number of right length
        if is_prime(n):
            return n

def is_prime(n, k=10):
    """Miller-Rabin primality test."""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as d * 2^r
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1
    
    # Perform k rounds of testing
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
            
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True

def extended_gcd(a, b):
    """Extended Euclidean Algorithm."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    """Calculate modular multiplicative inverse."""
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % m + m) % m

def int_to_bytes(n, length):
    """Convert integer to bytes with specified length."""
    return n.to_bytes(length, 'big')

def der_encode_integer(n):
    """Encode integer in DER format."""
    if n == 0:
        bytes_val = b'\x00'
    else:
        bytes_val = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    
    # Check bounds before accessing index
    if len(bytes_val) > 0 and bytes_val[0] & 0x80:  # Add padding if MSB is set
        bytes_val = b'\x00' + bytes_val
    
    length = len(bytes_val)
    if length < 128:
        return b'\x02' + bytes([length]) + bytes_val
    else:
        length_bytes = length.to_bytes((length.bit_length() + 7) // 8, 'big')
        return b'\x02' + bytes([0x80 | len(length_bytes)]) + length_bytes + bytes_val

def der_encode_sequence(data):
    """Encode sequence in DER format."""
    length = len(data)
    if length < 128:
        return b'\x30' + bytes([length]) + data
    else:
        length_bytes = length.to_bytes((length.bit_length() + 7) // 8, 'big')
        return b'\x30' + bytes([0x80 | len(length_bytes)]) + length_bytes + data

def create_private_key_der(key_params):
    """Create DER encoded private key."""
    n, e, d, p, q, dp, dq, qinv = key_params
    
    # RSA private key structure: SEQUENCE of version, n, e, d, p, q, dp, dq, qinv
    version = der_encode_integer(0)
    n_der = der_encode_integer(n)
    e_der = der_encode_integer(e)
    d_der = der_encode_integer(d)
    p_der = der_encode_integer(p)
    q_der = der_encode_integer(q)
    dp_der = der_encode_integer(dp)
    dq_der = der_encode_integer(dq)
    qinv_der = der_encode_integer(qinv)
    
    sequence_data = version + n_der + e_der + d_der + p_der + q_der + dp_der + dq_der + qinv_der
    return der_encode_sequence(sequence_data)

def create_public_key_der(n, e):
    """Create DER encoded public key."""
    # RSA public key structure: SEQUENCE of SEQUENCE of algorithm identifier, BIT STRING of public key
    
    # Algorithm identifier for RSA
    rsa_oid = b'\x06\x09\x2a\x86\x48\x86\xf7\x0d\x01\x01\x01'  # RSA OID
    null_param = b'\x05\x00'  # NULL parameters
    algorithm_id = der_encode_sequence(rsa_oid + null_param)
    
    # Public key bit string (SEQUENCE of n, e)
    n_der = der_encode_integer(n)
    e_der = der_encode_integer(e)
    public_key_seq = der_encode_sequence(n_der + e_der)
    
    # Bit string wrapper (unused bits = 0)
    bit_string = b'\x03' + der_encode_length(len(public_key_seq) + 1) + b'\x00' + public_key_seq
    
    # Final sequence
    return der_encode_sequence(algorithm_id + bit_string)

def der_encode_length(length):
    """Encode length in DER format."""
    if length < 128:
        return bytes([length])
    else:
        length_bytes = length.to_bytes((length.bit_length() + 7) // 8, 'big')
        return bytes([0x80 | len(length_bytes)]) + length_bytes

def pem_encode(der_data, label):
    """Encode DER data as PEM."""
    b64_data = base64.b64encode(der_data).decode('ascii')
    lines = [b64_data[i:i+64] for i in range(0, len(b64_data), 64)]
    return f"-----BEGIN {label}-----\n" + "\n".join(lines) + f"\n-----END {label}-----"

def generate_rsa_keypair(bits):
    """Generate RSA key pair."""
    # Generate two prime numbers
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    
    # Ensure p > q
    if p < q:
        p, q = q, p
    
    # Calculate n and φ(n)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose e (commonly 65537)
    e = 65537
    if gcd(e, phi) != 1:
        e = 3
        while gcd(e, phi) != 1:
            e += 2
    
    # Calculate d (private exponent)
    d = mod_inverse(e, phi)
    
    # Calculate CRT parameters
    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = mod_inverse(q, p)
    
    return (n, e, d, p, q, dp, dq, qinv)

def main():
    try:
        # Read input with bounds checking
        input_line = input().strip()
        if len(input_line) == 0:
            print("Error: No input provided", file=sys.stderr)
            return
        
        key_size = int(input_line)
        
        # Generate key pair
        key_params = generate_rsa_keypair(key_size)
        n, e = key_params[0], key_params[1]
        
        # Create DER encoded keys
        private_key_der = create_private_key_der(key_params)
        public_key_der = create_public_key_der(n, e)
        
        # Convert to PEM format
        private_key_pem = pem_encode(private_key_der, "RSA PRIVATE KEY")
        public_key_pem = pem_encode(public_key_der, "PUBLIC KEY")
        
        # Output
        print(private_key_pem)
        print()
        print(public_key_pem)
        
    except (ValueError, IndexError) as e:
        print(f"Error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()