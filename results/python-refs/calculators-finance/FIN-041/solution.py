numbers = list(map(float, input().split(',')))
mean = sum(numbers) / len(numbers)
print(f"{mean:.4f}")