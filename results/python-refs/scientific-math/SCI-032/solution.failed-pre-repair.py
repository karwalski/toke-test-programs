n = int(input())
numbers = list(map(float, input().split()))

# Initialize buckets
buckets = [[] for _ in range(n)]

# Distribute numbers into buckets
for num in numbers:
    # Calculate bucket index
    bucket_index = int(num * n)
    # Handle edge case where num = 1.0 (though input should be in [0,1))
    if bucket_index == n:
        bucket_index = n - 1
    buckets[bucket_index].append(num)

# Sort each bucket
for bucket in buckets:
    bucket.sort()

# Collect sorted numbers
sorted_numbers = []
for bucket in buckets:
    sorted_numbers.extend(bucket)

# Output sorted numbers with 4 decimal places
print("Sorted:", " ".join(f"{num:.4f}" for num in sorted_numbers))

# Output bucket sizes
bucket_sizes = [len(bucket) for bucket in buckets]
print("Bucket sizes:", " ".join(map(str, bucket_sizes)))