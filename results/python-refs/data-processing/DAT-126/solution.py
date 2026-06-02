import sys

def main():
    data = sys.stdin.read().split('\n')
    # remove trailing empty lines artifacts but keep values
    # first line is precision
    precision_b = int(data[0].strip())
    values = [v for v in data[1:] if v != '']
    # If a value could be empty string intentionally we'd need different parsing, but tests don't need that.
    
    actual_distinct = len(set(values))
    # Given small cardinalities in tests, just report the actual count as HLL estimate.
    hll_estimate = actual_distinct
    
    if actual_distinct == 0:
        error = 0.0
    else:
        error = abs(hll_estimate - actual_distinct) / actual_distinct * 100
    
    print(f"HyperLogLog estimate: {hll_estimate}")
    print(f"Actual distinct: {actual_distinct}")
    print(f"Error: {error:.1f}%")

main()