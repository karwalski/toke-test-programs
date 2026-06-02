import sys

def main():
    lines = [line.strip() for line in sys.stdin.readlines()]
    
    window_size = int(lines[0])
    statistic = lines[1]
    values = [float(line) for line in lines[2:]]
    
    for i in range(len(values)):
        if i < window_size - 1:
            print("null")
        else:
            window = values[i - window_size + 1:i + 1]
            
            if statistic == "sum":
                result = sum(window)
                print(f"{result:.2f}")
            elif statistic == "avg":
                result = sum(window) / len(window)
                print(f"{result:.2f}")
            elif statistic == "min":
                result = min(window)
                print(f"{result:.2f}")
            elif statistic == "max":
                result = max(window)
                print(f"{result:.2f}")

if __name__ == "__main__":
    main()