import sys

def main():
    data = sys.stdin.read().strip().split('\n')
    income = float(data[0].strip())
    brackets = []
    for line in data[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        t = float(parts[0])
        r = float(parts[1])
        brackets.append((t, r))
    brackets.sort(key=lambda x: x[0])
    tax = 0.0
    for i, (t, r) in enumerate(brackets):
        if i + 1 < len(brackets):
            upper = brackets[i+1][0]
        else:
            upper = float('inf')
        if income > t:
            taxable = min(income, upper) - t
            tax += taxable * r
        else:
            break
    print(f'{tax:.2f}')

main()
