import sys
import json

def decompose_time_series():
    lines = sys.stdin.read().strip().split('\n')
    period = int(lines[0])
    values = list(map(float, lines[1].split(',')))
    n = len(values)
    
    # Initialize components
    trend = [None] * n
    seasonal = [0] * n
    residual = [None] * n
    
    # Calculate trend using centered moving average
    half_period = period // 2
    for i in range(half_period, n - half_period):
        if period % 2 == 0:
            # Even period - need to average two centered values
            sum1 = sum(values[i - half_period:i + half_period])
            sum2 = sum(values[i - half_period + 1:i + half_period + 1])
            trend[i] = (sum1 + sum2) / (2 * period)
        else:
            # Odd period - simple centered average
            trend[i] = sum(values[i - half_period:i + half_period + 1]) / period
    
    # Calculate seasonal component
    # First, get detrended series
    detrended = []
    for i in range(n):
        if trend[i] is not None:
            detrended.append((i % period, values[i] - trend[i]))
    
    # Calculate average for each season
    season_sums = [0] * period
    season_counts = [0] * period
    
    for season_idx, detrended_val in detrended:
        season_sums[season_idx] += detrended_val
        season_counts[season_idx] += 1
    
    season_averages = []
    for i in range(period):
        if season_counts[i] > 0:
            season_averages.append(season_sums[i] / season_counts[i])
        else:
            season_averages.append(0)
    
    # Center the seasonal component (make sum = 0)
    season_mean = sum(season_averages) / period
    season_averages = [x - season_mean for x in season_averages]
    
    # Apply seasonal component to all observations
    for i in range(n):
        seasonal[i] = season_averages[i % period]
    
    # Calculate residuals
    for i in range(n):
        if trend[i] is not None:
            residual[i] = values[i] - trend[i] - seasonal[i]
    
    # Format output
    result = {
        "trend": trend,
        "seasonal": seasonal
    }
    
    print(json.dumps(result, separators=(',', ':')))

decompose_time_series()