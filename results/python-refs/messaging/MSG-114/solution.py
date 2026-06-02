import json
import sys

# Read input
lines = sys.stdin.read().strip().split('\n')
threats = json.loads(lines[0])
attachments = json.loads(lines[1])

# Process each attachment
for attachment in attachments:
    filename = attachment['filename']
    file_hash = attachment['hash']
    first_bytes = attachment['first_bytes']
    
    threat_found = False
    matched_threat = None
    
    # Check against each threat signature
    for threat in threats:
        threat_name = threat['name']
        threat_hash = threat['hash']
        threat_pattern = threat['pattern']
        
        # Check if both hash and pattern match
        if file_hash == threat_hash and first_bytes == threat_pattern:
            threat_found = True
            matched_threat = threat_name
            break
    
    # Output result
    if threat_found:
        print(f"{filename}: THREAT (matched: {matched_threat}, method: hash+pattern)")
    else:
        print(f"{filename}: CLEAN")