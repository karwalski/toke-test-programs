import sys, hashlib, hmac, struct

def clamp(k):
    k=bytearray(k); k[0]&=248; k[31]&=127; k[31]|=64; return bytes(k)

p = 2**255 - 19

def x25519(k, u):
    k=clamp(k)
    k_int=int.from_bytes(k,'little')
    u_int=int.from_bytes(u,'little') % p
    x1=u_int; x2=1; z2=0; x3=u_int; z3=1; swap=0
    a24=121665
    for t in range(254,-1,-1):
        kt=(k_int>>t)&1
        swap^=kt
        if swap: x2,x3=x3,x2; z2,z3=z3,z2
        swap=kt
        A=(x2+z2)%p; AA=A*A%p
        B=(x2-z2)%p; BB=B*B%p
        E=(AA-BB)%p
        C=(x3+z3)%p; D=(x3-z3)%p
        DA=D*A%p; CB=C*B%p
        x3=pow((DA+CB)%p,2,p)
        z3=x1*pow((DA-CB)%p,2,p)%p
        x2=AA*BB%p
        z2=E*((AA+a24*E)%p)%p
    if swap: x2,x3=x3,x2; z2,z3=z3,z2
    res=(x2*pow(z2,p-2,p))%p
    return res.to_bytes(32,'little')

def x25519_base(k):
    u=bytes([9])+b'\x00'*31
    return x25519(k,u)

def hkdf(chaining_key, ikm, num_outputs):
    tk = hmac.new(chaining_key, ikm, hashlib.sha256).digest()
    o1 = hmac.new(tk, b'\x01', hashlib.sha256).digest()
    o2 = hmac.new(tk, o1+b'\x02', hashlib.sha256).digest()
    if num_outputs==2: return o1,o2
    o3 = hmac.new(tk, o2+b'\x03', hashlib.sha256).digest()
    return o1,o2,o3

# ChaCha20-Poly1305
def rotl(x,n): return ((x<<n)&0xffffffff)|(x>>(32-n))
def qr(s,a,b,c,d):
    s[a]=(s[a]+s[b])&0xffffffff; s[d]=rotl(s[d]^s[a],16)
    s[c]=(s[c]+s[d])&0xffffffff; s[b]=rotl(s[b]^s[c],12)
    s[a]=(s[a]+s[b])&0xffffffff; s[d]=rotl(s[d]^s[a],8)
    s[c]=(s[c]+s[d])&0xffffffff; s[b]=rotl(s[b]^s[c],7)

def chacha20_block(key,counter,nonce):
    consts=[0x61707865,0x3320646e,0x79622d32,0x6b206574]
    keyw=list(struct.unpack('<8I',key))
    noncew=list(struct.unpack('<3I',nonce))
    state=consts+keyw+[counter]+noncew
    ws=list(state)
    for _ in range(10):
        qr(ws,0,4,8,12); qr(ws,1,5,9,13); qr(ws,2,6,10,14); qr(ws,3,7,11,15)
        qr(ws,0,5,10,15); qr(ws,1,6,11,12); qr(ws,2,7,8,13); qr(ws,3,4,9,14)
    out=bytes()
    for i in range(16):
        out+=struct.pack('<I',(ws[i]+state[i])&0xffffffff)
    return out

def chacha20(key,counter,nonce,data):
    out=bytearray()
    for i in range(0,len(data),64):
        blk=chacha20_block(key,counter+i//64,nonce)
        for j,b in enumerate(data[i:i+64]):
            out.append(b^blk[j])
    return bytes(out)

def poly1305_mac(msg,key):
    r=int.from_bytes(key[0:16],'little')
    r&=0x0ffffffc0ffffffc0ffffffc0fffffff
    s=int.from_bytes(key[16:32],'little')
    P=(1<<130)-5
    acc=0
    for i in range(0,len(msg),16):
        chunk=msg[i:i+16]
        n=int.from_bytes(chunk+b'\x01'+b'\x00'*(15-len(chunk)+1) if len(chunk)<16 else chunk+b'\x01','little')
        # simpler:
        block=chunk+b'\x01'
        if len(block)<17: block=block+b'\x00'*(17-len(block))
        n=int.from_bytes(block,'little')
        acc=((acc+n)*r)%P
    acc=(acc+s)&((1<<128)-1)
    return acc.to_bytes(16,'little')

def pad16(x):
    if len(x)%16==0: return b''
    return b'\x00'*(16-len(x)%16)

def chachapoly_encrypt(key,nonce_int,ad,plaintext):
    nonce=b'\x00'*4+nonce_int.to_bytes(8,'little')
    polykey=chacha20_block(key,0,nonce)[:32]
    ct=chacha20(key,1,nonce,plaintext)
    mac_data=ad+pad16(ad)+ct+pad16(ct)+struct.pack('<Q',len(ad))+struct.pack('<Q',len(ct))
    tag=poly1305_mac(mac_data,polykey)
    return ct+tag

class SymState:
    def __init__(self,name):
        self.h=name.encode().ljust(32,b'\x00') if len(name)<=32 else hashlib.sha256(name.encode()).digest()
        self.ck=self.h
        self.k=None; self.n=0
    def mix_hash(self,d):
        self.h=hashlib.sha256(self.h+d).digest()
    def mix_key(self,ikm):
        self.ck,k=hkdf(self.ck,ikm,2)
        self.k=k[:32]; self.n=0
    def encrypt_and_hash(self,pt):
        if self.k is None:
            self.mix_hash(pt); return pt
        ct=chachapoly_encrypt(self.k,self.n,self.h,pt)
        self.n+=1
        self.mix_hash(ct)
        return ct
    def split(self):
        k1,k2=hkdf(self.ck,b'',2)
        return k1[:32],k2[:32]

def main():
    lines=sys.stdin.read().split('\n')
    si=bytes.fromhex(lines[0].strip())
    sr_priv=bytes.fromhex(lines[1].strip())
    payload=lines[2].encode() if len(lines)>2 else b''
    SI_pub=x25519_base(si)
    SR_pub=x25519_base(sr_priv)
    # deterministic ephemerals
    ei=hashlib.sha256(b'eph_i'+si).digest()
    er=hashlib.sha256(b'eph_r'+sr_priv).digest()
    EI_pub=x25519_base(ei)
    ER_pub=x25519_base(er)
    ss=SymState('Noise_IK_25519_ChaChaPoly_SHA256')
    ss.mix_hash(b'')
    ss.mix_hash(SR_pub)  # prologue/rs known to initiator
    # message 1: e, es, s, ss
    ss.mix_hash(EI_pub)
    ss.mix_key(EI_pub)
    ss.mix_key(x25519(ei,SR_pub))  # es
    enc_s=ss.encrypt_and_hash(SI_pub)
    ss.mix_key(x25519(si,SR_pub))  # ss
    enc_p1=ss.encrypt_and_hash(payload)
    print('-> e, es, s, ss (message 1)')
    print('  ephemeral: '+EI_pub.hex())
    print('  encrypted_static: '+enc_s.hex())
    print('  encrypted_payload: '+enc_p1.hex())
    # message 2: e, ee, se
    ss.mix_hash(ER_pub)
    ss.mix_key(ER_pub)
    ss.mix_key(x25519(er,EI_pub))  # ee
    ss.mix_key(x25519(sr_priv,EI_pub))  # se
    enc_p2=ss.encrypt_and_hash(b'')
    print('<- e, ee, se (message 2)')
    print('  ephemeral: '+ER_pub.hex())
    print('  encrypted_payload: '+enc_p2.hex())
    k1,k2=ss.split()
    print('session keys:')
    print('  initiator_send: '+k1.hex())
    print('  initiator_recv: '+k2.hex())

main()
