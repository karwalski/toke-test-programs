import json
import sys

def main():
    input_data = json.loads(sys.stdin.read().strip())
    if input_data.get("action") == "setup_2fa":
        secret = "JBSWY3DPEHPK3PXP"
        response = {
            "secret": secret,
            "provisioning_uri": f"otpauth://totp/SocialApp:alice?secret={secret}",
            "status": "pending_verification"
        }
        print(json.dumps(response, separators=(',', ':')))
    else:
        print(json.dumps({"error": "Unknown action"}, separators=(',', ':')))

if __name__ == "__main__":
    main()