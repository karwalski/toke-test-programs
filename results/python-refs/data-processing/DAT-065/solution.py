import sys
from datetime import datetime, timedelta
from collections import defaultdict

def parse_frequency(freq_str):
    """Parse frequency string and return timedelta"""
    freq_map = {
        'hourly': timedelta(hours=1),
        'daily': timedelta(days=1),
        'minutely': timedelta(minutes=1),
        '15min': timedelta(minutes=15),
        '30min': timedelta(minutes=30)
    }
    return freq_map.get(freq_str)

def parse_timestamp(ts_str):
    """Parse ISO format timestamp"""
    return datetime.fromisoformat(ts_str)

def format_timestamp(dt):
    """Format datetime back to ISO string"""
    return dt.strftime('%Y-%m-%dT%H:%M')

def resample_timeseries():
    lines = sys.stdin.read().strip().split('\n')
    
    # Parse first line for frequency and aggregation
    freq_agg = lines[0].split()
    frequency = freq_agg[0]
    aggregation = freq_agg[1] if len(freq_agg) > 1 else 'mean'
    
    freq_delta = parse_frequency(frequency)
    if not freq_delta:
        return
    
    # Parse time series data
    data_points = []
    for line in lines[1:]:
        if line.strip():
            timestamp_str, value_str = line.split(',')
            timestamp = parse_timestamp(timestamp_str)
            value = float(value_str)
            data_points.append((timestamp, value))
    
    if not data_points:
        return
    
    # Sort by timestamp
    data_points.sort(key=lambda x: x[0])
    
    # Group data points by frequency bins
    bins = defaultdict(list)
    
    for timestamp, value in data_points:
        # Find the bin start time
        start_time = data_points[0][0]
        
        # Calculate which bin this timestamp belongs to
        time_diff = timestamp - start_time
        bin_number = int(time_diff.total_seconds() // freq_delta.total_seconds())
        bin_start = start_time + timedelta(seconds=bin_number * freq_delta.total_seconds())
        
        bins[bin_start].append(value)
    
    # Apply aggregation and output results
    for bin_start in sorted(bins.keys()):
        values = bins[bin_start]
        
        if aggregation == 'mean':
            result = sum(values) / len(values)
        elif aggregation == 'sum':
            result = sum(values)
        elif aggregation == 'min':
            result = min(values)
        elif aggregation == 'max':
            result = max(values)
        else:
            result = sum(values) / len(values)  # default to mean
        
        print(f"{format_timestamp(bin_start)},{result:.2f}")

resample_timeseries()