import os
import sys
import hashlib
import secrets
import subprocess
import tempfile

def main():
    # Read input
    mode = input().strip()
    input_file = input().strip()
    output_file = input().strip()
    passphrase = input().strip()
    
    try:
        if mode == "encrypt":
            # Use openssl command via subprocess for AES-256-CBC encryption
            with open(input_file, 'rb') as f:
                plaintext = f.read()
            
            # Create temporary file for openssl input
            with tempfile.NamedTemporaryFile(delete=False) as tmp_in:
                tmp_in.write(plaintext)
                tmp_in_path = tmp_in.name
            
            try:
                # Run openssl encryption
                result = subprocess.run([
                    'openssl', 'enc', '-aes-256-cbc', '-salt',
                    '-in', tmp_in_path,
                    '-out', output_file,
                    '-pass', f'pass:{passphrase}'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"Encrypted: {output_file}")
                else:
                    print(f"Encryption failed: {result.stderr}")
            finally:
                os.unlink(tmp_in_path)
                
        elif mode == "decrypt":
            # Use openssl command via subprocess for AES-256-CBC decryption
            result = subprocess.run([
                'openssl', 'enc', '-aes-256-cbc', '-d', '-salt',
                '-in', input_file,
                '-out', output_file,
                '-pass', f'pass:{passphrase}'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Decrypted: {output_file}")
            else:
                print(f"Decryption failed: {result.stderr}")
        else:
            print("Invalid mode. Use 'encrypt' or 'decrypt'")
            
    except FileNotFoundError:
        print(f"Error: File not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()