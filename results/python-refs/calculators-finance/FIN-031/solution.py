import sys

rates = []
for line in sys.stdin:
    line = line.strip()
    if line:
        date, rate = line.split()
        rates.append(float(rate))

average = sum(rates) / len(rates)
print(f"{average:.4f}")