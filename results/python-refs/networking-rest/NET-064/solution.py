import sys
import hashlib
import secrets

def generate_nonce():
    return secrets.token_hex(16)

def calculate_ha1(username, realm, password):
    return hashlib.md5(f"{username}:{realm}:{password}".encode()).hexdigest()

def calculate_ha2(method, uri):
    return hashlib.md5(f"{method}:{uri}".encode()).hexdigest()

def calculate_response(ha1, nonce, ha2):
    return hashlib.md5(f"{ha1}:{nonce}:{ha2}".encode()).hexdigest()

def main():
    lines = sys.stdin.read().strip().split('\n')
    port = lines[0]
    realm = lines[1]
    user_pass = lines[2].split(':')
    username = user_pass[0]
    password = user_pass[1]
    
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()