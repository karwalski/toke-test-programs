import sys

# Read input
line = input().strip()
parts = line.split()
prey_0 = int(parts[0])
pred_0 = int(parts[1])
alpha = float(parts[2])
beta = float(parts[3])
gamma = float(parts[4])
delta = float(parts[5])
steps = int(parts[6])

# Initialize populations
prey = float(prey_0)
pred = float(pred_0)

# Print initial state
print(f"0 {prey_0} {pred_0}")

# Simulate for N steps using Lotka-Volterra equations
for step in range(1, steps + 1):
    # Calculate derivatives
    dprey_dt = alpha * prey - beta * prey * pred
    dpred_dt = delta * prey * pred - gamma * pred
    
    # Update populations (using dt = 1)
    prey = prey + dprey_dt
    pred = pred + dpred_dt
    
    # Round to integers and print
    prey_rounded = round(prey)
    pred_rounded = round(pred)
    print(f"{step} {prey_rounded} {pred_rounded}")