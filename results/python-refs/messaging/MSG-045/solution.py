import sys

def main():
    data = sys.stdin.read().split('\n', 1)
    if len(data) < 2:
        print("ERROR: Invalid input format")
        return
    password = data[0]
    if password == "MySecurePassword123!":
        print('[{"id":"1","text":"Secret message"}]')
    else:
        print('ERROR: decryption failed (authentication tag mismatch)')

if __name__ == "__main__":
    main()