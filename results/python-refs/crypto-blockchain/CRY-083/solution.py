import sys, json, hashlib, hmac

def H(*parts):
    h = hashlib.sha256()
    for p in parts:
        if isinstance(p, str): p = p.encode()
        h.update(len(p).to_bytes(4,'big'))
        h.update(p)
    return h.digest()

def Hs(*parts):
    # hash to scalar (int)
    return int.from_bytes(H(*parts), 'big')

Q = (1<<256) - 189  # a large prime modulus for our toy group

def derive_seed(msg, signer_idx, priv_hex, pubs):
    # deterministic seed for the simulated randomness
    m = hashlib.sha256()
    m.update(msg.encode())
    m.update(str(signer_idx).encode())
    m.update(priv_hex.encode())
    for p in pubs:
        m.update(p.encode())
    return m.digest()

def prng(seed, idx):
    return hashlib.sha256(seed + b'|' + str(idx).encode()).digest()

def main():
    data = sys.stdin.read().split('\n')
    msg = data[0]
    signer = int(data[1])
    priv_hex = data[2].strip()
    pubs = json.loads(data[3])
    n = len(pubs)
    priv_int = int(priv_hex, 16) % Q
    pubs_int = [int(p,16) % Q for p in pubs]

    # key image: deterministic from private key and message-independent context
    ki_bytes = H(b'KI', priv_hex.encode(), b''.join(p.encode() for p in pubs))
    key_image = ki_bytes.hex()

    seed = derive_seed(msg, signer, priv_hex, pubs)

    # alpha = random scalar for signer's commitment
    alpha = int.from_bytes(prng(seed, 0), 'big') % Q

    s = [0]*n
    c = [0]*n

    # commitment for signer position
    L_signer = pow(2, alpha, Q)  # toy 'g^alpha'
    R_signer = Hs(b'HP', ki_bytes, str(alpha).encode()) % Q

    # next index after signer
    i = (signer + 1) % n
    c[i] = Hs(b'C', msg.encode(), key_image.encode(), L_signer.to_bytes(32,'big'), R_signer.to_bytes(32,'big'), str(i).encode()) % Q

    # walk around the ring
    j = i
    while j != signer:
        s[j] = int.from_bytes(prng(seed, j+1), 'big') % Q
        # L_j = g^s_j * P_j^c_j  (toy version)
        L_j = (pow(2, s[j], Q) * pow(pubs_int[j], c[j], Q)) % Q
        R_j = Hs(b'HP', ki_bytes, str(s[j]).encode(), str(c[j]).encode(), str(j).encode()) % Q
        nxt = (j+1) % n
        c[nxt] = Hs(b'C', msg.encode(), key_image.encode(), L_j.to_bytes(32,'big'), R_j.to_bytes(32,'big'), str(nxt).encode()) % Q
        j = nxt

    # close the ring at signer: s_signer = alpha - c_signer * priv  (mod Q)
    s[signer] = (alpha - c[signer] * priv_int) % Q

    out = {
        'key_image': key_image,
        'c0': format(c[0], '064x'),
        's_values': [format(x, '064x') for x in s]
    }
    print(json.dumps(out))

main()
