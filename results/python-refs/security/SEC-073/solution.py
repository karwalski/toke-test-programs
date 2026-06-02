import sys, hmac, hashlib, json, base64

def main():
    data = sys.stdin.read().split('\n')
    algo = data[0].strip()
    key = data[1] if len(data) > 1 else ''
    message = data[2] if len(data) > 2 else ''
    
    result = {}
    result['algorithm'] = algo
    
    if algo == 'HMAC-SHA256':
        h = hmac.new(key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)
        sig = h.hexdigest()
        result['keyType'] = 'HMAC'
        result['keyBits'] = len(key) * 8
        result['message_hash'] = hashlib.sha256(message.encode('utf-8')).hexdigest()
        result['signature_hex_prefix'] = sig[:16]
        result['valid'] = True
    elif algo == 'HMAC-SHA512':
        h = hmac.new(key.encode('utf-8'), message.encode('utf-8'), hashlib.sha512)
        sig = h.hexdigest()
        result['keyType'] = 'HMAC'
        result['keyBits'] = len(key) * 8
        result['message_hash'] = hashlib.sha512(message.encode('utf-8')).hexdigest()
        result['signature_hex_prefix'] = sig[:16]
        result['valid'] = True
    elif algo == 'SHA256':
        digest = hashlib.sha256(message.encode('utf-8')).hexdigest()
        result['keyType'] = 'none'
        result['keyBits'] = 0
        result['message_hash'] = digest
        result['signature_hex_prefix'] = digest[:16]
        result['valid'] = True
    else:
        result['valid'] = False
        result['keyType'] = 'unknown'
        result['keyBits'] = 0
        result['message_hash'] = ''
        result['signature_hex_prefix'] = ''
    
    print(json.dumps(result, sort_keys=True))

main()
