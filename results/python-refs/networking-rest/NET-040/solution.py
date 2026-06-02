import sys
import base64

def main():
    lines = sys.stdin.read().strip().split('\n')
    
    # Read port
    port = lines[0].strip()
    
    # Read realm name
    realm = lines[1].strip()
    
    # Read username:password pairs
    users = {}
    for i in range(2, len(lines)):
        line = lines[i].strip()
        if not line:
            break
        if ':' in line:
            username, password = line.split(':', 1)
            users[username] = password
    
    # Output the listening message
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()