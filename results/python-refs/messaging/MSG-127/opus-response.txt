import json
import sys

def main():
    data = sys.stdin.read().split('\n')
    relay_keys = json.loads(data[0])
    recipient = data[1]
    plaintext = data[2]
    
    n = len(relay_keys)
    lines = []
    for i, layer_num in enumerate(range(n, 0, -1)):
        relay_idx = i + 1
        if layer_num == n:
            lines.append(f"layer {layer_num} (outermost, for relay{relay_idx}):")
        else:
            lines.append(f"layer {layer_num} (for relay{relay_idx}):")
        if relay_idx == n:
            next_hop = "recipient"
        else:
            next_hop = f"relay{relay_idx + 1}"
        lines.append(f"  next_hop: {next_hop}")
        lines.append(f"  encrypted: base64")
    
    lines.append("layer 0 (for recipient):")
    lines.append(f"  plaintext: {plaintext}")
    
    print('\n'.join(lines))

main()