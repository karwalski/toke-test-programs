import sys
import json

def decompose_time_series():
    lines = sys.stdin.read().strip().split('\n')
    period = int(lines[0])
    values = list(map(float, lines[1].split(',')))
    n = len(values)
    
    trend = [None] * n
    seasonal = [0] * n
    
    half_period = period // 2
    if period % 2 == 0:
        # Centered moving average for even period
        for i in range(half_period, n - half_period):
            s = 0.5 * values[i - half_period] + 0.5 * values[i + half_period]
            for j in range(i - half_period + 1, i + half_period):
                s += values[j]
            trend[i] = s / period
    else:
        for i in range(half_period, n - half_period):
            trend[i] = sum(values[i - half_period:i + half_period + 1]) / period
    
    # Detrended
    season_sums = [0.0] * period
    season_counts = [0] * period
    for i in range(n):
        if trend[i] is not None:
            season_sums[i % period] += values[i] - trend[i]
            season_counts[i % period] += 1
    
    season_averages = [season_sums[i] / season_counts[i] if season_counts[i] > 0 else 0 for i in range(period)]
    season_mean = sum(season_averages) / period
    season_averages = [x - season_mean for x in season_averages]
    
    for i in range(n):
        seasonal[i] = season_averages[i % period]
    
    result = {"trend": trend, "seasonal": seasonal}
    print(json.dumps(result, separators=(',', ':')))

decompose_time_series()