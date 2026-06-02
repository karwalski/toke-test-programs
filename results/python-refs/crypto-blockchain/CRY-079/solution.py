import sys
import hashlib

def main():
    line = sys.stdin.readline().strip()
    parts = line.split()
    
    if parts[0] == "COMMIT":
        value = parts[1]
        nonce = parts[2]
        # Create commitment hash of value||nonce
        commitment_data = value + nonce
        commitment_hash = hashlib.sha256(commitment_data.encode()).hexdigest()
        print(commitment_hash)
        
    elif parts[0] == "VERIFY":
        value = parts[1]
        nonce = parts[2]
        commitment_hash = parts[3]
        # Recreate the hash from value||nonce
        commitment_data = value + nonce
        calculated_hash = hashlib.sha256(commitment_data.encode()).hexdigest()
        
        if calculated_hash == commitment_hash:
            print("VALID")
        else:
            print("INVALID")

if __name__ == "__main__":
    main()