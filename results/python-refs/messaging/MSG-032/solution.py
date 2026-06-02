import hmac
import hashlib

def derive_keys(chain_key_hex, num_keys):
    chain_key = bytes.fromhex(chain_key_hex)
    
    for step in range(1, num_keys + 1):
        # Derive message key using HMAC-SHA256 with constant 0x01
        message_key = hmac.new(chain_key, b'\x01', hashlib.sha256).digest()
        
        # Derive next chain key using HMAC-SHA256 with constant 0x02
        new_chain_key = hmac.new(chain_key, b'\x02', hashlib.sha256).digest()
        
        # Output in required format
        print(f"step {step}: ck={new_chain_key.hex()} mk={message_key.hex()}")
        
        # Update chain key for next iteration
        chain_key = new_chain_key

# Read input
chain_key_hex = input().strip()
num_keys = int(input().strip())

# Derive and output keys
derive_keys(chain_key_hex, num_keys)