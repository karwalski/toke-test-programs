import sys, hmac, hashlib, base64, json

SECRET = b'fixed-secret-key-for-csrf-demo'
FIXED_TS = 1700000000
EXPIRY = 3600

def gen_token(session_id, ts):
    msg = (session_id + str(ts)).encode('utf-8')
    mac = hmac.new(SECRET, msg, hashlib.sha256).digest()
    return base64.b64encode(mac).decode('ascii')

def main():
    data = sys.stdin.read().split('\n')
    if not data:
        print('INVALID: no input')
        return
    cmd = data[0].strip() if len(data) > 0 else ''
    sid = data[1].strip() if len(data) > 1 else ''
    if cmd == 'generate':
        if not sid:
            print('INVALID: missing session id')
            return
        token = gen_token(sid, FIXED_TS)
        out = {'token': token, 'expiresAt': FIXED_TS + EXPIRY}
        print(json.dumps(out, sort_keys=True))
    elif cmd == 'validate':
        if not sid:
            print('INVALID: missing session id')
            return
        if len(data) < 3 or not data[2].strip():
            print('INVALID: missing token')
            return
        provided = data[2].strip()
        expected = gen_token(sid, FIXED_TS)
        if hmac.compare_digest(provided, expected):
            print('VALID')
        else:
            print('INVALID: token mismatch')
    else:
        print('INVALID: unknown command')

main()
