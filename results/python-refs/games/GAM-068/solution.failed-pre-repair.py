import sys

def solve_poker_chips():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse denominations and counts
    chips_data = lines[0].split()
    chips = []
    for chip_info in chips_data:
        denom, count = chip_info.split(':')
        chips.append((int(denom), int(count)))
    
    # Sort chips by denomination in descending order
    chips.sort(reverse=True)
    
    # Process each amount
    for i in range(1, len(lines)):
        amount = int(lines[i])
        result = make_change(chips, amount)
        if result is None:
            print(f"{amount}: Cannot make amount")
        else:
            output_parts = [f"{amount}:"]
            for denom, used_count in result:
                if used_count > 0:
                    output_parts.append(f"{used_count}x{denom}")
            print(" ".join(output_parts))

def make_change(chips, amount):
    # Greedy approach: use largest denominations first
    result = []
    remaining = amount
    
    for denom, available_count in chips:
        if remaining == 0:
            break
        
        # Use as many of this denomination as possible
        use_count = min(remaining // denom, available_count)
        result.append((denom, use_count))
        remaining -= use_count * denom
    
    # If we couldn't make exact change, return None
    if remaining > 0:
        return None
    
    return result

solve_poker_chips()