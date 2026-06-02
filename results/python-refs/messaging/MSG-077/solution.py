import hashlib
import hmac

def derive_key(base_key_hex, message_number):
    """Derive a message-specific key using HMAC-SHA256"""
    # Ensure hex string has even length
    if len(base_key_hex) % 2 != 0:
        base_key_hex = '0' + base_key_hex
    
    base_key = bytes.fromhex(base_key_hex)
    message_bytes = str(message_number).encode('utf-8')
    derived = hmac.new(base_key, message_bytes, hashlib.sha256).hexdigest()
    return derived

def rotate_key(current_key_hex):
    """Generate next epoch key using SHA256"""
    # Ensure hex string has even length
    if len(current_key_hex) % 2 != 0:
        current_key_hex = '0' + current_key_hex
    
    current_key = bytes.fromhex(current_key_hex)
    next_key = hashlib.sha256(current_key).hexdigest()
    return next_key

def main():
    # Read input
    rotation_interval = int(input().strip())
    initial_secret = input().strip()
    num_messages = int(input().strip())
    
    current_epoch = 0
    current_base_key = initial_secret
    
    for msg_num in range(1, num_messages + 1):
        # Check if we need to rotate before this message
        if msg_num > 1 and (msg_num - 1) % rotation_interval == 0:
            # Rotate key
            print(f"[KEY ROTATION: epoch {current_epoch} -> {current_epoch + 1}]")
            current_epoch += 1
            current_base_key = rotate_key(current_base_key)
        
        # Derive message key
        message_key = derive_key(current_base_key, msg_num)
        key_preview = message_key[:6] + "..."
        
        # Output message info
        print(f"msg {msg_num}: epoch={current_epoch}, key={key_preview}")

if __name__ == "__main__":
    main()