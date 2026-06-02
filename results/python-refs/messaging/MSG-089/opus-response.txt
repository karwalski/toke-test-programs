import sys

def main():
    lines = sys.stdin.read().split('\n')
    pending_count = int(lines[3])
    
    print("RENEGOTIATION:")
    print(f"1. Suspend message delivery ({pending_count} pending)")
    print("2. Generate new ephemeral key")
    print("3. Send renegotiation request")
    print("4. Await acknowledgement")
    print("5. Derive new session key")
    if pending_count == 0:
        print("6. No pending messages to re-encrypt")
    else:
        print(f"6. Re-encrypt {pending_count} pending messages")
    print("7. Resume delivery")
    print("new_session: {key_hex, established_at}")

if __name__ == "__main__":
    main()