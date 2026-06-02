n = int(input())
v = int(input())

quorum_needed = (2 * n + 2) // 3  # This ensures we get ceiling of 2N/3

if v >= quorum_needed:
    print("QUORUM_REACHED")
else:
    needed = quorum_needed - v
    print(f"INSUFFICIENT (need {needed} more)")