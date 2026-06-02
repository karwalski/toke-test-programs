numbers = list(map(int, input().split()))

print("Initial:", " ".join(map(str, numbers)))

n = len(numbers)
for i in range(n - 1):
    swapped = False
    for j in range(n - 1 - i):
        if numbers[j] > numbers[j + 1]:
            numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
            swapped = True
    
    if not swapped:
        break
    
    print(f"Pass {i + 1}:", " ".join(map(str, numbers)))

print("Sorted:", " ".join(map(str, numbers)))