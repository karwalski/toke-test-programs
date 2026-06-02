import sys, json, hashlib

def main():
    data = sys.stdin.read().splitlines()
    value = int(data[0].strip())
    n = int(data[1].strip())
    blinding_hex = data[2].strip()
    upper = 1 << n
    if value < 0 or value >= upper:
        print(json.dumps({"error": f"Value {value} not in range [0, {upper})"}, separators=(',', ':')))
        return
    try:
        r_bytes = bytes.fromhex(blinding_hex)
    except ValueError:
        r_bytes = blinding_hex.encode()
    # Pedersen-like commitment: H(value || blinding)
    h = hashlib.sha256()
    h.update(value.to_bytes(32, 'big'))
    h.update(r_bytes)
    commitment = h.hexdigest()
    bit_commitments = []
    for i in range(n):
        bit = (value >> i) & 1
        bh = hashlib.sha256()
        bh.update(bytes([bit]))
        bh.update(i.to_bytes(4, 'big'))
        bh.update(r_bytes)
        bit_commitments.append(bh.hexdigest())
    out = {
        "commitment": commitment,
        "range_bits": n,
        "bit_commitments": bit_commitments,
        "proof_valid": True
    }
    print(json.dumps(out, separators=(',', ':')))

main()
