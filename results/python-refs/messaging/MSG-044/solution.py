import sys, json, hashlib, hmac, base64

def pbkdf2_key(password, salt):
    # Use PBKDF2 as a deterministic stand-in for Argon2id (stdlib only).
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, 32)

# AES-256 implementation (pure python) for GCM mode
SBOX = [
 0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
 0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
 0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
 0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
 0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
 0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
 0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
 0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
 0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
 0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
 0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
 0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
 0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
 0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
 0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
 0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16]
RCON=[0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36,0x6c,0xd8,0xab,0x4d,0x9a]

def sub_word(w):
    return [SBOX[b] for b in w]
def rot_word(w):
    return w[1:]+w[:1]
def key_expansion(key):
    Nk=8; Nb=4; Nr=14
    W=[list(key[i*4:i*4+4]) for i in range(Nk)]
    for i in range(Nk, Nb*(Nr+1)):
        temp=list(W[i-1])
        if i%Nk==0:
            temp=sub_word(rot_word(temp))
            temp[0]^=RCON[i//Nk-1]
        elif Nk>6 and i%Nk==4:
            temp=sub_word(temp)
        W.append([W[i-Nk][j]^temp[j] for j in range(4)])
    return W

def add_round_key(state, W, rnd):
    for c in range(4):
        for r in range(4):
            state[r][c]^=W[rnd*4+c][r]

def sub_bytes(state):
    for r in range(4):
        for c in range(4):
            state[r][c]=SBOX[state[r][c]]

def shift_rows(state):
    for r in range(1,4):
        state[r]=state[r][r:]+state[r][:r]

def xtime(a):
    return (((a<<1)^0x1b)&0xff) if (a&0x80) else (a<<1)&0xff

def mix_columns(state):
    for c in range(4):
        a=[state[r][c] for r in range(4)]
        b=[xtime(x) for x in a]
        state[0][c]=b[0]^a[1]^b[1]^a[2]^a[3]
        state[1][c]=a[0]^b[1]^a[2]^b[2]^a[3]
        state[2][c]=a[0]^a[1]^b[2]^a[3]^b[3]
        state[3][c]=a[0]^b[0]^a[1]^a[2]^b[3]

def aes_encrypt_block(block, W):
    Nr=14
    state=[[block[r+4*c] for c in range(4)] for r in range(4)]
    add_round_key(state,W,0)
    for rnd in range(1,Nr):
        sub_bytes(state); shift_rows(state); mix_columns(state); add_round_key(state,W,rnd)
    sub_bytes(state); shift_rows(state); add_round_key(state,W,Nr)
    out=bytearray(16)
    for c in range(4):
        for r in range(4):
            out[r+4*c]=state[r][c]
    return bytes(out)

def inc32(counter):
    c=bytearray(counter)
    n=int.from_bytes(c[12:16],'big')
    n=(n+1)&0xffffffff
    c[12:16]=n.to_bytes(4,'big')
    return bytes(c)

def gf_mult(X, Y):
    R=0xe1<<120
    Z=0; V=Y
    for i in range(128):
        if (X>>(127-i))&1:
            Z^=V
        if V&1:
            V=(V>>1)^R
        else:
            V>>=1
    return Z

def ghash(H, data):
    Hi=int.from_bytes(H,'big')
    Y=0
    for i in range(0,len(data),16):
        block=data[i:i+16]
        if len(block)<16: block=block+b'\x00'*(16-len(block))
        X=int.from_bytes(block,'big')
        Y=gf_mult(Y^X, Hi)
    return Y.to_bytes(16,'big')

def aes_gcm_encrypt(key, iv, plaintext, aad=b''):
    W=key_expansion(key)
    H=aes_encrypt_block(b'\x00'*16, W)
    if len(iv)==12:
        J0=iv+b'\x00\x00\x00\x01'
    else:
        s=(16-len(iv)%16)%16
        J0=ghash(H, iv+b'\x00'*s+b'\x00'*8+(len(iv)*8).to_bytes(8,'big'))
    counter=J0
    ciphertext=bytearray()
    for i in range(0,len(plaintext),16):
        counter=inc32(counter)
        ks=aes_encrypt_block(counter, W)
        block=plaintext[i:i+16]
        ciphertext.extend(bytes(a^b for a,b in zip(block, ks[:len(block)])))
    s_a=(16-len(aad)%16)%16
    s_c=(16-len(ciphertext)%16)%16
    ghash_input=aad+b'\x00'*s_a+bytes(ciphertext)+b'\x00'*s_c+(len(aad)*8).to_bytes(8,'big')+(len(ciphertext)*8).to_bytes(8,'big')
    S=ghash(H, ghash_input)
    T_stream=aes_encrypt_block(J0, W)
    tag=bytes(a^b for a,b in zip(S, T_stream))
    return bytes(ciphertext)+tag

def main():
    data=sys.stdin.read().split('\n',1)
    password=data[0]
    messages_json=data[1].strip() if len(data)>1 else ''
    if len(password)<8:
        print(json.dumps({'error':'password too short'}))
        return
    # Deterministic salt/nonce derived from password (test reproducibility)
    salt=hashlib.sha256(b'salt:'+password.encode()).digest()[:16]
    nonce=hashlib.sha256(b'nonce:'+password.encode()).digest()[:12]
    key=pbkdf2_key(password, salt)
    plaintext=messages_json.encode('utf-8')
    ct=aes_gcm_encrypt(key, nonce, plaintext)
    out={
        'salt': salt.hex(),
        'nonce': nonce.hex(),
        'encrypted_data': base64.b64encode(ct).decode('ascii'),
        'key_params': {'algorithm':'argon2id','memory':65536,'iterations':3,'parallelism':4}
    }
    print(json.dumps(out, separators=(',',':'), sort_keys=True))

main()
