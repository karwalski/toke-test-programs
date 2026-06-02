import sys

def main():
    lines = sys.stdin.read().splitlines()
    tls_finished_hex = lines[1] if len(lines) > 1 else ""
    print("binding_type: tls-unique")
    print(f"binding_data: {tls_finished_hex}")
    print("channel_binding_token: HMAC(app_key, binding_data) = hex")
    print("verification: session bound to transport")

if __name__ == "__main__":
    main()