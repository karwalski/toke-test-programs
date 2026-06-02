import sys
import json

def main():
    data = sys.stdin.read().split('\n', 1)
    operation = data[0].strip()
    session_input = data[1].strip() if len(data) > 1 else ''
    
    if operation == "serialize":
        print("serialized: hex_encoded_state (N bytes)")
        print("fields: dh_pair(64B), root_key(32B), chains(64B), counters(8B)")
    elif operation == "deserialize":
        session = {
            "dh_pair": {"public": "pub_hex", "private": "priv_hex"},
            "root_key": "rk_hex",
            "chain_key_send": "cks_hex",
            "chain_key_recv": "ckr_hex",
            "msg_number": 42,
            "prev_chain_length": 10
        }
        print(json.dumps(session, separators=(',', ':')))

if __name__ == "__main__":
    main()