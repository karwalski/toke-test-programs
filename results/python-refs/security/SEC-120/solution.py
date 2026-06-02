import sys
import json
import base64
import urllib.request
import urllib.parse
import time
from urllib.error import URLError, HTTPError

def test_padding_oracle(url_template, cipher_b64):
    try:
        # Decode the base64 ciphertext
        cipher_bytes = base64.b64decode(cipher_b64)
    except:
        return {"oracle_detected": False, "oracle_type": None, "evidence": "Invalid base64", "severity": "none"}
    
    # Store baseline response
    baseline_response = None
    baseline_time = None
    baseline_status = None
    
    # Test original ciphertext first
    try:
        encoded_cipher = urllib.parse.quote(cipher_b64)
        test_url = url_template.replace('{CIPHER}', encoded_cipher)
        
        start_time = time.time()
        with urllib.request.urlopen(test_url) as response:
            baseline_response = response.read().decode('utf-8', errors='ignore')
            baseline_status = response.status
        baseline_time = time.time() - start_time
    except HTTPError as e:
        baseline_status = e.code
        try:
            baseline_response = e.read().decode('utf-8', errors='ignore')
        except:
            baseline_response = ""
        baseline_time = time.time() - start_time
    except:
        return {"oracle_detected": False, "oracle_type": None, "evidence": "Connection failed", "severity": "none"}
    
    # Test modified ciphertexts
    different_responses = []
    timing_diffs = []
    
    for i in range(min(len(cipher_bytes), 8)):  # Test first 8 bytes max
        modified_cipher = bytearray(cipher_bytes)
        modified_cipher[i] = (modified_cipher[i] + 1) % 256
        
        try:
            modified_b64 = base64.b64encode(modified_cipher).decode()
            encoded_modified = urllib.parse.quote(modified_b64)
            test_url = url_template.replace('{CIPHER}', encoded_modified)
            
            start_time = time.time()
            try:
                with urllib.request.urlopen(test_url) as response:
                    test_response = response.read().decode('utf-8', errors='ignore')
                    test_status = response.status
                test_time = time.time() - start_time
            except HTTPError as e:
                test_status = e.code
                try:
                    test_response = e.read().decode('utf-8', errors='ignore')
                except:
                    test_response = ""
                test_time = time.time() - start_time
            
            # Check for different responses
            if test_response != baseline_response or test_status != baseline_status:
                different_responses.append({
                    'byte_pos': i,
                    'status': test_status,
                    'response': test_response[:100]  # Truncate for brevity
                })
            
            # Check timing differences
            if baseline_time and abs(test_time - baseline_time) > 0.1:
                timing_diffs.append({
                    'byte_pos': i,
                    'time_diff': test_time - baseline_time
                })
                
        except:
            continue
    
    # Analyze results
    if different_responses:
        # Check for padding-related error messages
        for resp in different_responses:
            response_lower = resp['response'].lower()
            if any(keyword in response_lower for keyword in ['padding', 'decrypt', 'invalid', 'bad']):
                return {
                    "oracle_detected": True,
                    "oracle_type": "error_message",
                    "evidence": f"Different error messages detected: {resp['response'][:50]}",
                    "severity": "high"
                }
        
        return {
            "oracle_detected": True,
            "oracle_type": "padding",
            "evidence": f"Different responses for {len(different_responses)} modified bytes",
            "severity": "medium"
        }
    
    if len(timing_diffs) >= 2:
        return {
            "oracle_detected": True,
            "oracle_type": "timing",
            "evidence": f"Timing differences detected: avg {sum(d['time_diff'] for d in timing_diffs)/len(timing_diffs):.3f}s",
            "severity": "medium"
        }
    
    return {
        "oracle_detected": False,
        "oracle_type": None,
        "evidence": "No oracle behavior detected",
        "severity": "none"
    }

def main():
    lines = sys.stdin.read().strip().split('\n')
    url_template = lines[0]
    cipher_b64 = lines[1]
    
    result = test_padding_oracle(url_template, cipher_b64)
    
    print("oracle_detected")

if __name__ == "__main__":
    main()