import sys
import struct
import random

def encode_websocket_frame():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    direction = lines[0]
    frame_type = lines[1]
    payload = lines[2]
    
    # Convert payload to bytes
    if frame_type in ['text', 'ping', 'pong', 'close']:
        payload_bytes = payload.encode('utf-8')
    else:  # binary
        payload_bytes = payload.encode('utf-8')  # For simplicity, treat as UTF-8
    
    payload_len = len(payload_bytes)
    
    # Set FIN bit and opcode
    first_byte = 0x80  # FIN = 1
    
    if frame_type == 'text':
        first_byte |= 0x1
    elif frame_type == 'binary':
        first_byte |= 0x2
    elif frame_type == 'close':
        first_byte |= 0x8
    elif frame_type == 'ping':
        first_byte |= 0x9
    elif frame_type == 'pong':
        first_byte |= 0xA
    
    frame = bytearray([first_byte])
    
    # Set mask bit and length
    mask_bit = 1 if direction == 'client' else 0
    
    if payload_len < 126:
        second_byte = (mask_bit << 7) | payload_len
        frame.append(second_byte)
    elif payload_len < 65536:
        second_byte = (mask_bit << 7) | 126
        frame.append(second_byte)
        frame.extend(struct.pack('>H', payload_len))
    else:
        second_byte = (mask_bit << 7) | 127
        frame.append(second_byte)
        frame.extend(struct.pack('>Q', payload_len))
    
    # Add masking key and masked payload if client
    if direction == 'client':
        mask_key = struct.pack('>I', random.randint(0, 0xFFFFFFFF))
        frame.extend(mask_key)
        
        masked_payload = bytearray()
        for i, byte in enumerate(payload_bytes):
            masked_payload.append(byte ^ mask_key[i % 4])
        
        frame.extend(masked_payload)
        
        # Output format
        hex_parts = []
        hex_parts.append(f"{frame[0]:02X}")
        hex_parts.append(f"{frame[1]:02X}")
        hex_parts.append("[mask4]")
        hex_parts.append("[masked_payload]")
        
        opcode = frame[0] & 0x0F
        opcode_names = {0x1: 'text', 0x2: 'binary', 0x8: 'close', 0x9: 'ping', 0xA: 'pong'}
        opcode_name = opcode_names.get(opcode, 'unknown')
        
        print(" ".join(hex_parts))
        print(f"FIN=1, opcode=0x{opcode:X} ({opcode_name}), MASK=1, len={payload_len}")
    else:
        # Server frame (no masking)
        frame.extend(payload_bytes)
        
        hex_parts = []
        for byte in frame:
            hex_parts.append(f"{byte:02X}")
        
        opcode = frame[0] & 0x0F
        opcode_names = {0x1: 'text', 0x2: 'binary', 0x8: 'close', 0x9: 'ping', 0xA: 'pong'}
        opcode_name = opcode_names.get(opcode, 'unknown')
        
        print(" ".join(hex_parts))
        print(f"FIN=1, opcode=0x{opcode:X} ({opcode_name}), MASK=0, len={payload_len}")

encode_websocket_frame()