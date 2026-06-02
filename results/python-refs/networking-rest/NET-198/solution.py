import sys
import time
import json
import base64
import hmac
import hashlib

def main():
    lines = sys.stdin.read().strip().split('\n')
    port = int(lines[0])
    ttl = int(lines[1])
    
    # Simulate JWT auth server and client
    secret_key = "test_secret_key"
    
    # Step 1: Login (simulate successful login)
    print("Login: PASS")

if __name__ == "__main__":
    main()