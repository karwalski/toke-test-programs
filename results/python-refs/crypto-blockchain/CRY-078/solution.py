import json
import sys

def validate_certificate_chain():
    try:
        # Read input from stdin
        input_data = sys.stdin.read().strip()
        certificates = json.loads(input_data)
        
        if not certificates:
            print("ERROR: Empty certificate chain at position 0")
            return
        
        # Validate each certificate
        for i, cert in enumerate(certificates):
            # Check required fields
            required_fields = ["subject", "issuer", "signature", "public_key"]
            for field in required_fields:
                if field not in cert:
                    print(f"ERROR: Missing {field} at position {i}")
                    return
            
            # Find the issuer certificate
            issuer_cert = None
            
            # Look for issuer in the chain
            for issuer_candidate in certificates:
                if issuer_candidate["subject"] == cert["issuer"]:
                    issuer_cert = issuer_candidate
                    break
            
            # If no issuer found
            if issuer_cert is None:
                print(f"ERROR: Issuer not found at position {i}")
                return
            
            # Validate signature (simplified validation - checking if signature is "valid")
            if cert["signature"] != "valid":
                print(f"ERROR: Invalid signature at position {i}")
                return
        
        # If we get here, all certificates are valid
        print("VALID")
        
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON format at position 0")
    except Exception as e:
        print("ERROR: Invalid input at position 0")

if __name__ == "__main__":
    validate_certificate_chain()