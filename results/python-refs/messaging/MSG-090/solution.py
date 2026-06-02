import sys, hmac, hashlib, json

def main():
    data = sys.stdin.read().splitlines()
    msg_hash = data[0].strip()
    priv_key_hex = data[1].strip()
    timestamp = data[2].strip()
    priv_key = bytes.fromhex(priv_key_hex)
    sig_input = (msg_hash + timestamp).encode('utf-8')
    recipient_sig = hmac.new(priv_key, sig_input, hashlib.sha256).hexdigest()
    prev_receipt_hash = '0' * 64
    chain_input = (msg_hash + recipient_sig + timestamp + prev_receipt_hash).encode('utf-8')
    receipt_hash = hashlib.sha256(chain_input).hexdigest()
    receipt = {
        'msg_hash': msg_hash,
        'recipient_sig': recipient_sig,
        'timestamp': timestamp,
        'receipt_hash': receipt_hash
    }
    print(json.dumps(receipt, separators=(',', ':'), sort_keys=False))

main()
