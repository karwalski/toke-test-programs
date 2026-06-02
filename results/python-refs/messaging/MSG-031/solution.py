import sys, hashlib, hmac, json

def hkdf_extract(salt, ikm):
    return hmac.new(salt, ikm, hashlib.sha256).digest()

def hkdf_expand(prk, info, length):
    okm = b''
    t = b''
    i = 1
    while len(okm) < length:
        t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
        okm += t
        i += 1
    return okm[:length]

def hkdf(salt, ikm, info, length):
    return hkdf_expand(hkdf_extract(salt, ikm), info, length)

def sim_dh(k1, k2):
    # Simulated DH: hash of sorted concatenation
    a, b = sorted([k1, k2])
    return hashlib.sha256(a + b).digest()

def main():
    lines = sys.stdin.read().strip().split('\n')
    ik_a = bytes.fromhex(lines[0].strip())
    ik_b = bytes.fromhex(lines[1].strip())
    spk_b = bytes.fromhex(lines[2].strip())
    opk_b = bytes.fromhex(lines[3].strip())

    # X3DH: ephemeral key derived deterministically from inputs for reproducibility
    ek_a = hashlib.sha256(b'EK_A' + ik_a + ik_b).digest()

    dh1 = sim_dh(ik_a, spk_b)
    dh2 = sim_dh(ek_a, ik_b)
    dh3 = sim_dh(ek_a, spk_b)
    dh4 = sim_dh(ek_a, opk_b)

    shared_secret = dh1 + dh2 + dh3 + dh4

    salt = b'\x00' * 32
    info = b'X3DH-SHA256'
    session_key = hkdf(salt, shared_secret, info, 32)

    associated_data = ik_a + ik_b

    out = {
        'shared_secret': shared_secret.hex(),
        'session_key': session_key.hex(),
        'associated_data': associated_data.hex()
    }
    print(json.dumps(out))

main()
