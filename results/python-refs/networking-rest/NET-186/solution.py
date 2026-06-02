import urllib.request
import urllib.parse
import time
import sys

def make_request(url, use_gzip=False):
    headers = {}
    if use_gzip:
        headers['Accept-Encoding'] = 'gzip'
    
    req = urllib.request.Request(url, headers=headers)
    
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read()
            end_time = time.time()
            return len(data), end_time - start_time
    except:
        return 0, 0

def main():
    url = input().strip()
    
    # Make request without compression
    uncompressed_size, uncompressed_time = make_request(url, use_gzip=False)
    
    # Make request with compression
    compressed_size, compressed_time = make_request(url, use_gzip=True)
    
    # Calculate compression ratio
    if compressed_size > 0:
        compression_ratio = uncompressed_size / compressed_size
    else:
        compression_ratio = 1.0
    
    print("Compression ratio:")

if __name__ == "__main__":
    main()