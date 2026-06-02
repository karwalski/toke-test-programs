import sys, json, hmac, hashlib

def main():
    data = sys.stdin.read().split('\n')
    priv_hex = data[0].strip()
    message = data[1]
    ta_json = json.loads(data[2])
    timestamp = ta_json['time']
    ta_sig = ta_json['ta_signature']
    key = bytes.fromhex(priv_hex)
    # signer signs content + timestamp
    signer_payload = (message + '|' + timestamp).encode('utf-8')
    signer_sig = hmac.new(key, signer_payload, hashlib.sha256).hexdigest()
    # combined hash binds content, timestamp, signer_sig, ta_sig
    combined_input = (message + '|' + timestamp + '|' + signer_sig + '|' + ta_sig).encode('utf-8')
    combined_hash = hashlib.sha256(combined_input).hexdigest()
    bundle = {
        'content': message,
        'signer_sig': signer_sig,
        'timestamp': timestamp,
        'ta_sig': ta_sig,
        'combined_hash': combined_hash
    }
    print(json.dumps(bundle, separators=(',', ':')))

main()
