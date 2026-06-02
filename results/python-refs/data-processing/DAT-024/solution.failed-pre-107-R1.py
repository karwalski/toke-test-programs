def lsd_radix_sort():
    # Read input
    numbers = list(map(int, input().split()))
    
    # Find the maximum number to determine number of digits
    max_num = max(numbers)
    max_digits = len(str(max_num))
    
    # Current list of numbers being sorted
    current_numbers = numbers[:]
    
    # Process each digit position
    for digit_pos in range(max_digits):
        # Create 10 buckets for digits 0-9
        buckets = [[] for _ in range(10)]
        
        # Place numbers into buckets based on current digit
        for num in current_numbers:
            digit = (num // (10 ** digit_pos)) % 10
            buckets[digit].append(num)
        
        # Print the pass
        digit_names = ["ones", "tens", "hundreds", "thousands"]
        digit_name = digit_names[digit_pos] if digit_pos < len(digit_names) else f"10^{digit_pos}"
        
        print(f"Pass {digit_pos + 1} ({digit_name}):", end="")
        
        for i, bucket in enumerate(buckets):
            if bucket:
                bucket_str = ",".join(map(str, bucket))
                if i == 0:
                    print(f" [{bucket_str}]", end="")
                else:
                    print(f" [{i}:{bucket_str}]", end="")
        
        print(" ...")
        
        # Collect numbers from buckets in order
        current_numbers = []
        for bucket in buckets:
            current_numbers.extend(bucket)
    
    # Print sorted result
    print(f"Sorted: {' '.join(map(str, current_numbers))}")

lsd_radix_sort()