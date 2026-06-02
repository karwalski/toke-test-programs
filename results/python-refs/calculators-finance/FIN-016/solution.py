import sys

# Read input
line = input().strip()
face_value, coupon_rate, yield_rate, periods = line.split()

face_value = float(face_value)
coupon_rate = float(coupon_rate)
yield_rate = float(yield_rate)
periods = int(periods)

# Calculate coupon payment
coupon_payment = face_value * coupon_rate

# Calculate present value of coupon payments
pv_coupons = 0
for i in range(1, periods + 1):
    pv_coupons += coupon_payment / ((1 + yield_rate) ** i)

# Calculate present value of face value
pv_face_value = face_value / ((1 + yield_rate) ** periods)

# Calculate bond price
bond_price = pv_coupons + pv_face_value

# Output to 2 decimal places
print(f"{bond_price:.2f}")