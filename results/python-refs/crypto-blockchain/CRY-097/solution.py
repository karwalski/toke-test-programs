import json
import sys

# Read input
pool_balance = int(input().strip())
borrow_amount = int(input().strip())
fee_percent = float(input().strip())
operations_json = input().strip()

# Parse operations
operations = json.loads(operations_json)

# Calculate fee
fee = borrow_amount * fee_percent / 100
repay_amount = borrow_amount + fee

# Execute operations
current_balance = borrow_amount
for operation in operations:
    if operation["type"] == "buy":
        # Use amount to buy, get return back
        current_balance = current_balance - operation["amount"] + operation["return"]
    elif operation["type"] == "sell":
        # Use amount to sell, get return back
        current_balance = current_balance - operation["amount"] + operation["return"]

# Check if we can repay
if current_balance >= repay_amount:
    profit_loss = int(current_balance - repay_amount)
    result = "SUCCESS"
else:
    profit_loss = int(current_balance - repay_amount)
    result = "FAILED: insufficient repayment"

print(profit_loss)
print(result)