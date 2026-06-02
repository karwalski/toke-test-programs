import json
import sys

# Read input
lock_params = json.loads(input().strip())
current_time = int(input().strip())
action = input().strip()

beneficiary = lock_params["beneficiary"]
amount = lock_params["amount"]
lock_until = lock_params["lock_until"]

if action == "withdraw":
    if current_time >= lock_until:
        print(f"SUCCESS: {beneficiary} withdraws {amount}")
    else:
        remaining = lock_until - current_time
        print(f"LOCKED ({remaining} seconds remaining)")
elif action == "check":
    if current_time >= lock_until:
        print("UNLOCKED")
    else:
        print("LOCKED")