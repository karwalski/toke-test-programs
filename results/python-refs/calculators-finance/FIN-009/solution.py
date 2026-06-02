line = input().strip()
parts = line.split()
mode = parts[0]
num1 = float(parts[1])
num2 = float(parts[2])

if mode == 'of':
    result = (num1 / 100) * num2
    if result == int(result):
        print(int(result))
    else:
        print(result)
elif mode == 'change':
    result = ((num2 - num1) / num1) * 100
    if result == int(result):
        print(f"{int(result)}%")
    else:
        print(f"{result}%")
elif mode == 'what':
    result = (num1 / num2) * 100
    if result == int(result):
        print(f"{int(result)}%")
    else:
        print(f"{result}%")