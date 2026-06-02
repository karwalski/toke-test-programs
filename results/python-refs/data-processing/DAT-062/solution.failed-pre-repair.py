import sys

def main():
    # Read window size and alpha
    first_line = input().strip().split()
    window_size = int(first_line[0])
    alpha = float(first_line[1])
    
    values = []
    
    # Read all values
    for line in sys.stdin:
        line = line.strip()
        if line:
            values.append(float(line))
    
    # Process each period
    for i in range(len(values)):
        # Simple Moving Average
        if i + 1 < window_size:
            sma = "null"
        else:
            window_values = values[i - window_size + 1:i + 1]
            sma = f"{sum(window_values) / window_size:.2f}"
        
        # Exponential Moving Average
        if i == 0:
            ema = values[0]
            if i + 1 < window_size:
                ema_str = "null"
            else:
                ema_str = f"{ema:.2f}"
        else:
            ema = alpha * values[i] + (1 - alpha) * ema
            if i + 1 < window_size:
                ema_str = "null"
            else:
                ema_str = f"{ema:.2f}"
        
        # Weighted Moving Average
        if i + 1 < window_size:
            wma = "null"
        else:
            window_values = values[i - window_size + 1:i + 1]
            weights = list(range(1, window_size + 1))
            weighted_sum = sum(w * v for w, v in zip(weights, window_values))
            weight_sum = sum(weights)
            wma = f"{weighted_sum / weight_sum:.2f}"
        
        print(f"{sma}\t{ema_str}\t{wma}")

if __name__ == "__main__":
    main()