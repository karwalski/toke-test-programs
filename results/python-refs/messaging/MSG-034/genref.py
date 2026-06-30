#!/usr/bin/env python3
"""MSG-034 reference + fixture generator (114.27 / ADR-faithful Signal numeric fingerprint).

Implements Signal's NumericFingerprintGenerator algorithm faithfully:

  perParty(key, id):
    h = SHA512( shortBE(FINGERPRINT_VERSION=0) || key || id )
    repeat ITERATIONS (5200): h = SHA512( h || key )
    fp = h[0:30]
    digits = concat over 6 chunks of 5 bytes: "%05d" % (byteArray5ToLong(chunk) % 100000)
  combined = order-independent: smaller(localDigits, remoteDigits) + larger  (lexicographic)
  output  = combined grouped into 12 space-separated groups of 5 digits

This matches the libsignal source (FINGERPRINT_VERSION=0, 5200 iterations, 5-byte
big-endian chunks mod 100000, lexicographic ordering of the two 30-digit strings).

The corpus uses the documented simplification: the supplied hex keys are the raw
public key bytes (no 0x05 DJB type-prefix). The validate() oracle below proves the
core algorithm against libsignal's published test vector WITH the 0x05 prefix.
"""
import hashlib

FINGERPRINT_VERSION = 0
ITERATIONS = 5200


def _short_be(v):
    return bytes([(v >> 8) & 0xFF, v & 0xFF])


def _fingerprint(key, identifier):
    # libsignal: hash_0 = version || key || id (raw, NOT pre-hashed); then each
    # of ITERATIONS rounds is hash = SHA512(hash || key).
    h = _short_be(FINGERPRINT_VERSION) + key + identifier
    for _ in range(ITERATIONS):
        h = hashlib.sha512(h + key).digest()
    return h[:30]


def _byte_array_5_to_long(b, off):
    return ((b[off] & 0xFF) << 32) | ((b[off + 1] & 0xFF) << 24) | \
           ((b[off + 2] & 0xFF) << 16) | ((b[off + 3] & 0xFF) << 8) | (b[off + 4] & 0xFF)


def _display_digits(fp):
    out = ""
    for off in range(0, 30, 5):
        out += "%05d" % (_byte_array_5_to_long(fp, off) % 100000)
    return out  # 30 digits


def safety_number(key_a, id_a, key_b, id_b):
    """key_* are bytes (already-decoded), id_* are bytes. Returns the 60-digit
    number grouped into 12 space-separated groups of 5."""
    da = _display_digits(_fingerprint(key_a, id_a))
    db = _display_digits(_fingerprint(key_b, id_b))
    combined = (da + db) if da <= db else (db + da)
    return " ".join(combined[i:i + 5] for i in range(0, 60, 5))


def safety_number_hex(key_a_hex, id_a, key_b_hex, id_b):
    return safety_number(bytes.fromhex(key_a_hex), id_a.encode("utf-8"),
                         bytes.fromhex(key_b_hex), id_b.encode("utf-8"))


# ── Provenance oracle: libsignal NumericFingerprintGeneratorTest vector ──────
# Identity keys include the 0x05 DJB type byte (33 bytes), stable ids are phone
# numbers, 5200 iterations. Expected displayable fingerprint is published.
ALICE_IDENTITY = bytes([
    0x05, 0x06, 0x86, 0x3b, 0xc6, 0x6d, 0x02, 0xb4, 0x0d, 0x27, 0xb8, 0xd4, 0x9c,
    0xa7, 0xc0, 0x9e, 0x92, 0x39, 0x23, 0x6f, 0x9d, 0x7d, 0x25, 0xd6, 0xfc, 0xca,
    0x5c, 0xe1, 0x3c, 0x70, 0x64, 0xd8, 0x68])
BOB_IDENTITY = bytes([
    0x05, 0xf7, 0x81, 0xb6, 0xfb, 0x32, 0xfe, 0xd9, 0xba, 0x1c, 0xf2, 0xde, 0x97,
    0x8d, 0x4d, 0x5d, 0xa2, 0x8d, 0xc3, 0x40, 0x46, 0xae, 0x19, 0xb5, 0xf6, 0x85,
    0x9b, 0xed, 0xa8, 0xcf, 0x47, 0x1f, 0xa8])
ALICE_ID = b"+14152222222"
BOB_ID = b"+14153333333"
EXPECTED_DISPLAYABLE = "300354477692869396892869876765458257569162576843440918079131"
# Alice is the lexicographically-smaller party, so the first 30 digits of the
# published displayable fingerprint are Alice's per-party number. This is the
# rigorous oracle for the whole hash+encode pipeline (version 0, 5200 iterations,
# 30-byte truncation, 5-byte big-endian chunk mod 100000, %05d).
EXPECTED_ALICE_HALF = EXPECTED_DISPLAYABLE[:30]


def validate():
    alice = _display_digits(_fingerprint(ALICE_IDENTITY, ALICE_ID))
    ok_alice = (alice == EXPECTED_ALICE_HALF)
    print("ORACLE alice-half", "PASS" if ok_alice else "FAIL")
    print("  expected:", EXPECTED_ALICE_HALF)
    print("  got:     ", alice)
    # order-independence: swapping the two parties yields the identical number.
    fwd = safety_number_hex(
        "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef", "alice@example.com",
        "fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210", "bob@example.com")
    rev = safety_number_hex(
        "fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210", "bob@example.com",
        "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef", "alice@example.com")
    ok_order = (fwd == rev)
    print("ORACLE order-independence", "PASS" if ok_order else "FAIL")
    return ok_alice and ok_order


if __name__ == "__main__":
    validate()
    print("\n--- corpus fixtures ---")
    cases = [
        ("0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef", "alice@example.com",
         "fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210", "bob@example.com"),
        ("00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff", "carol@example.com",
         "ffeeddccbbaa99887766554433221100ffeeddccbbaa99887766554433221100", "dave@example.com"),
        # order-swap of case 1 — must equal case 1
        ("fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210", "bob@example.com",
         "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef", "alice@example.com"),
    ]
    for i, (ka, ia, kb, ib) in enumerate(cases, 1):
        print(f"case{i}: {safety_number_hex(ka, ia, kb, ib)}")
