import json
import hashlib
import base64
import secrets

def xor_encrypt(data, key):
    """Simple XOR encryption using the key cyclically"""
    key_bytes = bytes.fromhex(key)
    data_bytes = data.encode('utf-8') if isinstance(data, str) else data
    result = bytearray()
    for i, byte in enumerate(data_bytes):
        result.append(byte ^ key_bytes[i % len(key_bytes)])
    return bytes(result)

def generate_thumbnail_data(filename, mime_type):
    """Generate a simple thumbnail representation"""
    if mime_type.startswith('image/'):
        return f"thumbnail_data_for_{filename}_64x64"
    else:
        return f"file_icon_for_{filename}"

def main():
    # Read input
    filename = input().strip()
    file_size = int(input().strip())
    mime_type = input().strip()
    content_hash = input().strip()
    encryption_key = input().strip()
    
    # Generate thumbnail data
    thumbnail = generate_thumbnail_data(filename, mime_type)
    
    # Create metadata to encrypt
    metadata = {
        "filename": filename,
        "mime_type": mime_type,
        "thumbnail": thumbnail
    }
    
    # Convert metadata to JSON string
    metadata_json = json.dumps(metadata, separators=(',', ':'))
    
    # Encrypt the metadata
    encrypted_metadata_bytes = xor_encrypt(metadata_json, encryption_key)
    encrypted_metadata_b64 = base64.b64encode(encrypted_metadata_bytes).decode('ascii')
    
    # Generate key hash
    key_hash = hashlib.sha256(bytes.fromhex(encryption_key)).hexdigest()
    
    # Create output
    output = {
        "encrypted_metadata": encrypted_metadata_b64,
        "content_hash": content_hash,
        "size": file_size,
        "key_hash": key_hash
    }
    
    # Output JSON
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()