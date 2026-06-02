difficulty = float(input())
block_time = float(input())

hashrate = difficulty * (2**32) * 1000 / block_time
print(f"{hashrate:.2e}")