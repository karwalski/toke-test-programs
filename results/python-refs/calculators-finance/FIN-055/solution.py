window_size = int(input())
values = list(map(float, input().split(',')))

moving_averages = []
for i in range(len(values) - window_size + 1):
    window = values[i:i + window_size]
    avg = sum(window) / window_size
    moving_averages.append(f"{avg:.2f}")

print(','.join(moving_averages))