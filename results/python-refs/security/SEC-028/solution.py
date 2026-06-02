import sys
import re

def parse_http_request(request_text):
    lines = request_text.strip().split('\n')
    if not lines:
        return None, {}, ""
    
    request_line = lines[0]
    headers = {}
    body_start = len(lines)
    
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "":
            body_start = i + 1
            break
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip().lower()] = value.strip()
    
    body = '\n'.join(lines[body_start:]) if body_start < len(lines) else ""
    return request_line, headers, body

def check_chunked_encoding_malformed(body):
    if not body.strip():
        return False
    
    lines = body.split('\n')
    i = 0
    while i < len(lines):
        chunk_size_line = lines[i].strip()
        if not chunk_size_line:
            i += 1
            continue
        
        # Try to parse chunk size
        try:
            chunk_size = int(chunk_size_line, 16)
        except ValueError:
            return True  # Malformed chunk size
        
        if chunk_size == 0:
            # End chunk
            return False
        
        # Check if we have enough lines for the chunk data
        if i + 1 >= len(lines):
            return True  # Missing chunk data
        
        chunk_data = lines[i + 1]
        if len(chunk_data) != chunk_size:
            return True  # Chunk size mismatch
        
        i += 2
    
    return False

def analyze_request(request_text):
    request_line, headers, body = parse_http_request(request_text)
    
    if not request_line:
        return "SAFE", ""
    
    content_length = headers.get('content-length')
    transfer_encoding = headers.get('transfer-encoding')
    
    has_cl = content_length is not None
    has_te = transfer_encoding is not None
    is_chunked = has_te and 'chunked' in transfer_encoding.lower()
    
    # Check for conflicting headers
    if has_cl and has_te:
        if is_chunked:
            # Both CL and TE:chunked present - this is CL.TE vulnerability
            return "VULNERABLE", "CL.TE"
        else:
            # Both CL and TE present but not chunked - this is TE.CL vulnerability  
            return "VULNERABLE", "TE.CL"
    
    # Check for malformed chunked encoding
    if is_chunked and check_chunked_encoding_malformed(body):
        return "VULNERABLE", "TE.TE"
    
    # Check for multiple Transfer-Encoding headers (TE.TE)
    if has_te and transfer_encoding.count(',') > 0:
        return "VULNERABLE", "TE.TE"
    
    return "SAFE", ""

def main():
    input_text = sys.stdin.read()
    requests = input_text.split('---')
    
    for request in requests:
        request = request.strip()
        if not request:
            continue
            
        status, attack_type = analyze_request(request)
        
        if status == "VULNERABLE":
            print(attack_type)
        else:
            print("SAFE")

if __name__ == "__main__":
    main()