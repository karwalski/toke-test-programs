import sys

# Read hex-encoded frame bytes
hex_input = input().strip()
frame_bytes = bytes.fromhex(hex_input.replace(' ', ''))

# Parse first byte: FIN (1 bit) + RSV (3 bits) + opcode (4 bits)
first_byte = frame_bytes[0]
fin = (first_byte & 0x80) >> 7
rsv = (first_byte & 0x70) >> 4
opcode = first_byte & 0x0F

# Parse second byte: MASK (1 bit) + payload length (7 bits)
second_byte = frame_bytes[1]
mask_bit = (second_byte & 0x80) >> 7
payload_length = second_byte & 0x7F

# Opcode mapping
opcode_names = {
    0x0: "continuation",
    0x1: "text", 
    0x2: "binary",
    0x8: "close",
    0x9: "ping",
    0xA: "pong"
}

opcode_name = opcode_names.get(opcode, f"unknown(0x{opcode:x})")

# Handle extended payload length
offset = 2
if payload_length == 126:
    payload_length = int.from_bytes(frame_bytes[2:4], 'big')
    offset = 4
elif payload_length == 127:
    payload_length = int.from_bytes(frame_bytes[2:10], 'big')
    offset = 10

# Handle masking key
mask_key = None
if mask_bit:
    mask_key = frame_bytes[offset:offset+4]
    offset += 4

# Extract payload
payload_bytes = frame_bytes[offset:offset+payload_length]

# Unmask payload if masked
if mask_bit and mask_key:
    unmasked_payload = bytearray()
    for i in range(len(payload_bytes)):
        unmasked_payload.append(payload_bytes[i] ^ mask_key[i % 4])
    payload_bytes = bytes(unmasked_payload)

# Decode payload as text
try:
    payload_text = payload_bytes.decode('utf-8')
except:
    payload_text = str(payload_bytes)

# Format RSV
rsv_str = f"{rsv:03b}"

# Format mask
mask_str = "yes" if mask_bit else "no"

# Output
print(f'FIN={fin}, RSV={rsv_str}, opcode={opcode_name}(0x{opcode:x}), mask={mask_str}, length={payload_length}, payload="{payload_text}"')