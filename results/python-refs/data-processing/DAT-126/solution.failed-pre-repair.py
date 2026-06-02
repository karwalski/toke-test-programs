import hashlib
import sys

def hyperloglog(precision_b, values):
    m = 2 ** precision_b  # Number of buckets
    buckets = [0] * m
    
    for value in values:
        # Hash the value
        hash_value = hashlib.sha1(str(value).encode()).hexdigest()
        # Convert to integer
        hash_int = int(hash_value, 16)
        
        # Get the first b bits for bucket index
        bucket_idx = hash_int & (m - 1)
        
        # Get remaining bits and count leading zeros + 1
        remaining_bits = hash_int >> precision_b
        leading_zeros = 0
        
        # Count leading zeros in the remaining bits
        bit_pos = 1
        while bit_pos <= remaining_bits and (remaining_bits & bit_pos) == 0:
            leading_zeros += 1
            bit_pos <<= 1
            if leading_zeros >= 64:  # Prevent infinite loop
                break
        
        # Update bucket with max leading zeros + 1
        buckets[bucket_idx] = max(buckets[bucket_idx], leading_zeros + 1)
    
    # Calculate raw estimate
    raw_estimate = (0.7213 / (1 + 1.079/m)) * m * m / sum(2**(-x) for x in buckets)
    
    # Apply small range correction if needed
    if raw_estimate <= 2.5 * m:
        zeros = buckets.count(0)
        if zeros != 0:
            estimate = m * (1.0 / zeros) * 0.693147  # m * ln(m/V)
        else:
            estimate = raw_estimate
    else:
        estimate = raw_estimate
    
    return int(round(estimate))

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

precision_b = int(lines[0])
values = lines[1:]

# Calculate HyperLogLog estimate
hll_estimate = hyperloglog(precision_b, values)

# Calculate actual distinct count
actual_distinct = len(set(values))

# Calculate error
if actual_distinct == 0:
    error = 0.0
else:
    error = abs(hll_estimate - actual_distinct) / actual_distinct * 100

print(f"HyperLogLog estimate: {hll_estimate}")
print(f"Actual distinct: {actual_distinct}")
print(f"Error: {error:.1f}%")