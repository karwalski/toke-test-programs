import hashlib
import hmac
import sys

def mnemonic_to_seed(mnemonic, passphrase=""):
    # BIP39 seed generation using PBKDF2
    # The salt is "mnemonic" + passphrase
    salt = ("mnemonic" + passphrase).encode('utf-8')
    
    # Use PBKDF2 with HMAC-SHA512, 2048 iterations, 64-byte output
    seed = hashlib.pbkdf2_hmac('sha512', mnemonic.encode('utf-8'), salt, 2048, 64)
    
    return seed.hex()

# Read input from stdin
lines = sys.stdin.read().strip().split('\n')
mnemonic = lines[0].strip()
passphrase = lines[1].strip() if len(lines) > 1 else ""

# Generate and output the seed
seed_hex = mnemonic_to_seed(mnemonic, passphrase)
print(seed_hex)