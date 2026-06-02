def sum_of_proper_divisors(n):
    if n <= 1:
        return 0
    divisor_sum = 1  # 1 is always a proper divisor
    i = 2
    while i * i <= n:
        if n % i == 0:
            divisor_sum += i
            if i * i != n:  # avoid counting square root twice
                divisor_sum += n // i
        i += 1
    return divisor_sum

def find_amicable_pairs(n):
    pairs = []
    seen = set()
    
    for i in range(2, n + 1):
        if i in seen:
            continue
            
        sum_i = sum_of_proper_divisors(i)
        
        if sum_i > i and sum_i <= n:  # only check if sum_i > i to avoid duplicates
            sum_sum_i = sum_of_proper_divisors(sum_i)
            if sum_sum_i == i:  # amicable pair found
                pairs.append((i, sum_i))
                seen.add(i)
                seen.add(sum_i)
    
    return pairs

n = int(input())
pairs = find_amicable_pairs(n)

for pair in pairs:
    print(f"Pairs: {pair}")

count = len(pairs)
if count == 1:
    print(f"Count: {count} pairs.")
else:
    print(f"Count: {count} pairs.")