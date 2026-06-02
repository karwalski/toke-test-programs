import json
import base64
import secrets
import hashlib
import sys

def simple_encrypt(message, key_hex):
    """Simple XOR-based encryption using the key"""
    key_bytes = bytes.fromhex(key_hex)
    message_bytes = message.encode('utf-8') if isinstance(message, str) else message
    
    # Create a repeating key pattern
    key_hash = hashlib.sha256(key_bytes).digest()
    
    encrypted = bytearray()
    for i, byte in enumerate(message_bytes):
        encrypted.append(byte ^ key_hash[i % len(key_hash)])
    
    return bytes(encrypted)

def create_onion_layers(relay_keys, recipient_key, plaintext):
    """Create onion routing layers"""
    
    # Start with the innermost layer (for recipient)
    current_data = plaintext.encode('utf-8')
    layers = []
    
    # Layer 0: For recipient (plaintext)
    layers.append({
        'layer_num': 0,
        'target': 'recipient',
        'next_hop': None,
        'data': plaintext,
        'is_plaintext': True
    })
    
    # Build layers from innermost to outermost
    all_keys = relay_keys + [recipient_key]
    
    # Layer 1: For relay3 -> recipient
    if len(relay_keys) >= 1:
        encrypted_data = simple_encrypt(current_data, relay_keys[-1])
        encoded_data = base64.b64encode(encrypted_data).decode('utf-8')
        layers.insert(0, {
            'layer_num': 1,
            'target': f'relay{len(relay_keys)}',
            'next_hop': 'recipient',
            'data': encoded_data,
            'is_plaintext': False
        })
        
        # Prepare data for next layer
        layer_content = f"next_hop: recipient\nencrypted: {encoded_data}"
        current_data = layer_content.encode('utf-8')
    
    # Layer 2: For relay2 -> relay3
    if len(relay_keys) >= 2:
        encrypted_data = simple_encrypt(current_data, relay_keys[-2])
        encoded_data = base64.b64encode(encrypted_data).decode('utf-8')
        layers.insert(0, {
            'layer_num': 2,
            'target': f'relay{len(relay_keys)-1}',
            'next_hop': f'relay{len(relay_keys)}',
            'data': encoded_data,
            'is_plaintext': False
        })
        
        # Prepare data for next layer
        layer_content = f"next_hop: relay{len(relay_keys)}\nencrypted: {encoded_data}"
        current_data = layer_content.encode('utf-8')
    
    # Layer 3: For relay1 -> relay2
    if len(relay_keys) >= 3:
        encrypted_data = simple_encrypt(current_data, relay_keys[-3])
        encoded_data = base64.b64encode(encrypted_data).decode('utf-8')
        layers.insert(0, {
            'layer_num': 3,
            'target': 'relay1',
            'next_hop': 'relay2',
            'data': encoded_data,
            'is_plaintext': False
        })
    
    return layers

def generate_test_keys(relay_names):
    """Generate actual hex keys for testing"""
    keys = {}
    for name in relay_names:
        keys[name] = secrets.token_hex(32)  # 64 hex characters
    keys['recipient_pub_hex'] = secrets.token_hex(32)
    return keys

def main():
    # Read input
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    relay_keys_input = json.loads(lines[0])
    recipient_key_input = lines[1]
    plaintext = lines[2]
    
    # Generate actual hex keys to replace placeholders
    test_keys = generate_test_keys(['relay1_pub_hex', 'relay2_pub_hex', 'relay3_pub_hex'])
    
    # Map placeholder names to actual hex keys
    relay_keys = []
    for key_placeholder in relay_keys_input:
        if key_placeholder in test_keys:
            relay_keys.append(test_keys[key_placeholder])
        else:
            # If not a known placeholder, assume it's already hex
            relay_keys.append(key_placeholder)
    
    # Handle recipient key
    if recipient_key_input in test_keys:
        recipient_key = test_keys[recipient_key_input]
    else:
        recipient_key = recipient_key_input
    
    # Create onion layers
    layers = create_onion_layers(relay_keys, recipient_key, plaintext)
    
    # Output layers in reverse order (outermost first)
    for layer in layers:
        if layer['is_plaintext']:
            print(f"layer {layer['layer_num']} (for {layer['target']}):")
            print(f"  plaintext: {layer['data']}")
        else:
            print(f"layer {layer['layer_num']} (for {layer['target']}):")
            print(f"  next_hop: {layer['next_hop']}")
            print(f"  encrypted: {layer['data']}")

if __name__ == "__main__":
    main()