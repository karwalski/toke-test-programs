import json
import sys

def detect_nonce_reuse():
    # Read JSON from stdin
    input_data = sys.stdin.read()
    operations = json.loads(input_data)
    
    # Track nonce usage: (key_id, nonce) -> first_use_index
    nonce_usage = {}
    
    for i, op in enumerate(operations):
        if op["operation"] == "encrypt":
            key_id = op["key_id"]
            nonce = op["nonce_hex"]
            key_nonce_pair = (key_id, nonce)
            
            if key_nonce_pair in nonce_usage:
                # Nonce reuse detected - output severity and exit
                print("CRITICAL")
                return
            else:
                # First use of this key-nonce pair
                nonce_usage[key_nonce_pair] = i

if __name__ == "__main__":
    detect_nonce_reuse()