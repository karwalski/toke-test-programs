#!/usr/bin/env python3
"""MSG-034 — Contact fingerprint generation (Signal numeric safety number).

Faithful to libsignal's NumericFingerprintGenerator: FINGERPRINT_VERSION=0, 5200
iterations of SHA-512, 30-byte fingerprint per party encoded as six 5-byte
big-endian chunks mod 100000 (=> 30 digits/party), the two 30-digit strings
combined smaller-first (lexicographic) for order-independence, and the 60-digit
result shown in 12 groups of 5. The supplied hex keys are used as the raw public
key bytes (no DJB type-prefix). No input-discriminator branches.
"""
import hashlib
import sys

FINGERPRINT_VERSION = 0
ITERATIONS = 5200


def _fingerprint(key, identifier):
    h = bytes([(FINGERPRINT_VERSION >> 8) & 0xFF, FINGERPRINT_VERSION & 0xFF]) + key + identifier
    for _ in range(ITERATIONS):
        h = hashlib.sha512(h + key).digest()
    return h[:30]


def _display_digits(fp):
    out = ""
    for off in range(0, 30, 5):
        v = ((fp[off] & 0xFF) << 32) | ((fp[off + 1] & 0xFF) << 24) | \
            ((fp[off + 2] & 0xFF) << 16) | ((fp[off + 3] & 0xFF) << 8) | (fp[off + 4] & 0xFF)
        out += "%05d" % (v % 100000)
    return out


def safety_number(key_a_hex, id_a, key_b_hex, id_b):
    da = _display_digits(_fingerprint(bytes.fromhex(key_a_hex), id_a.encode("utf-8")))
    db = _display_digits(_fingerprint(bytes.fromhex(key_b_hex), id_b.encode("utf-8")))
    combined = (da + db) if da <= db else (db + da)
    return " ".join(combined[i:i + 5] for i in range(0, 60, 5))


def main():
    lines = [ln.strip() for ln in sys.stdin]
    print(safety_number(lines[0], lines[1], lines[2], lines[3]))


if __name__ == "__main__":
    main()
