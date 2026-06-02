import sys
import json
import hmac
import hashlib
import time
import base64
from urllib.parse import parse_qs, urlparse

def main():
    lines = sys.stdin.read().strip().split('\n')
    port = lines[0]
    secret = lines[1]
    
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()