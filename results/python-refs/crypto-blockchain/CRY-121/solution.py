import json
import sys

def decode_address(hex_str):
    # Remove 0x prefix and leading zeros, then take last 40 characters (20 bytes)
    addr = hex_str[2:].zfill(64)[-40:]
    # Remove leading zeros for display
    return addr.lstrip('0') or '0'

def decode_amount(hex_str):
    # Remove 0x prefix and convert to integer
    return int(hex_str, 16)

def main():
    # Read JSON from stdin
    input_data = sys.stdin.read().strip()
    receipt = json.loads(input_data)
    
    # Transfer event signature hash
    transfer_sig = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
    
    for log in receipt.get("logs", []):
        topics = log.get("topics", [])
        data = log.get("data", "")
        
        # Check if this is a Transfer event
        if len(topics) >= 3 and topics[0] == transfer_sig:
            from_addr = decode_address(topics[1])
            to_addr = decode_address(topics[2])
            amount = decode_amount(data)
            
            print(f"{from_addr} -> {to_addr}: {amount}")

if __name__ == "__main__":
    main()