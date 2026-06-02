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

# Calculate present value of each cash flow and weighted time
total_pv = 0
weighted_time_pv = 0

# Present value of coupon payments
for t in range(1, periods + 1):
    pv_coupon = coupon_payment / ((1 + yield_rate) ** t)
    total_pv += pv_coupon
    weighted_time_pv += t * pv_coupon

# Present value of face value at maturity
pv_face = face_value / ((1 + yield_rate) ** periods)
total_pv += pv_face
weighted_time_pv += periods * pv_face

# Calculate Macaulay duration
macaulay_duration = weighted_time_pv / total_pv

# Calculate modified duration
modified_duration = macaulay_duration / (1 + yield_rate)

# Output results to 4 decimal places
print(f"{macaulay_duration:.4f}")
print(f"{modified_duration:.4f}")