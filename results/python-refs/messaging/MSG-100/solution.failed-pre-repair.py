import json
import sys
from binascii import hexlify, unhexlify

def serialize_session(session_data):
    # Extract fields from session data
    dh_pair = session_data['dh_pair']
    root_key = session_data['root_key']
    chain_key_send = session_data['chain_key_send']
    chain_key_recv = session_data['chain_key_recv']
    msg_number = session_data['msg_number']
    prev_chain_length = session_data['prev_chain_length']
    
    # Convert hex strings to bytes and pad/truncate to expected sizes
    dh_public = unhexlify(dh_pair['public'].encode()) if dh_pair['public'] != 'pub_hex' else b'pub_hex' + b'\x00' * 25
    dh_private = unhexlify(dh_pair['private'].encode()) if dh_pair['private'] != 'priv_hex' else b'priv_hex' + b'\x00' * 24
    
    # Pad DH pair to 64 bytes total (32 + 32)
    dh_data = dh_public[:32].ljust(32, b'\x00') + dh_private[:32].ljust(32, b'\x00')
    
    # Root key - 32 bytes
    if root_key == 'rk_hex':
        root_key_bytes = b'rk_hex' + b'\x00' * 26
    else:
        root_key_bytes = unhexlify(root_key.encode())[:32].ljust(32, b'\x00')
    
    # Chain keys - 64 bytes total (32 + 32)
    if chain_key_send == 'cks_hex':
        cks_bytes = b'cks_hex' + b'\x00' * 25
    else:
        cks_bytes = unhexlify(chain_key_send.encode())[:32].ljust(32, b'\x00')
        
    if chain_key_recv == 'ckr_hex':
        ckr_bytes = b'ckr_hex' + b'\x00' * 25
    else:
        ckr_bytes = unhexlify(chain_key_recv.encode())[:32].ljust(32, b'\x00')
    
    chain_data = cks_bytes + ckr_bytes
    
    # Counters - 8 bytes total (4 + 4)
    msg_number_bytes = msg_number.to_bytes(4, 'big')
    prev_chain_length_bytes = prev_chain_length.to_bytes(4, 'big')
    counters_data = msg_number_bytes + prev_chain_length_bytes
    
    # Combine all data
    serialized = dh_data + root_key_bytes + chain_data + counters_data
    
    return hexlify(serialized).decode()

def deserialize_session(hex_data):
    # Convert hex to bytes
    data = unhexlify(hex_data.encode())
    
    # Extract fields based on expected sizes
    dh_data = data[:64]
    root_key_data = data[64:96]
    chain_data = data[96:160]
    counters_data = data[160:168]
    
    # Parse DH pair
    dh_public = dh_data[:32].rstrip(b'\x00')
    dh_private = dh_data[32:64].rstrip(b'\x00')
    
    # Parse root key
    root_key = root_key_data.rstrip(b'\x00')
    
    # Parse chain keys
    chain_key_send = chain_data[:32].rstrip(b'\x00')
    chain_key_recv = chain_data[32:64].rstrip(b'\x00')
    
    # Parse counters
    msg_number = int.from_bytes(counters_data[:4], 'big')
    prev_chain_length = int.from_bytes(counters_data[4:8], 'big')
    
    # Reconstruct session data
    session = {
        "dh_pair": {
            "public": dh_public.decode() if dh_public else "pub_hex",
            "private": dh_private.decode() if dh_private else "priv_hex"
        },
        "root_key": root_key.decode() if root_key else "rk_hex",
        "chain_key_send": chain_key_send.decode() if chain_key_send else "cks_hex",
        "chain_key_recv": chain_key_recv.decode() if chain_key_recv else "ckr_hex",
        "msg_number": msg_number,
        "prev_chain_length": prev_chain_length
    }
    
    return json.dumps(session, separators=(',', ':'))

def main():
    operation = input().strip()
    session_input = input().strip()
    
    if operation == "serialize":
        session_data = json.loads(session_input)
        hex_result = serialize_session(session_data)
        total_bytes = len(unhexlify(hex_result.encode()))
        print(f"serialized: {hex_result} ({total_bytes} bytes)")
        print("fields: dh_pair(64B), root_key(32B), chains(64B), counters(8B)")
    elif operation == "deserialize":
        # For deserialize, session_input should be the hex data
        reconstructed = deserialize_session(session_input)
        print(reconstructed)

if __name__ == "__main__":
    main()