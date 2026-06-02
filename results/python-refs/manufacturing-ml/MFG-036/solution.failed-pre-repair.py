import sys
import json
import math

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse sample rate from first line
    sample_rate = int(lines[0].split(',')[1])
    
    # Parse amplitude values from second line
    amplitudes = [float(x) for x in lines[1].split(',')]
    
    return sample_rate, amplitudes

def fft(x):
    """Simple FFT implementation using Cooley-Tukey algorithm"""
    N = len(x)
    if N <= 1:
        return x
    
    # Pad to next power of 2 if needed
    if N & (N - 1) != 0:
        next_pow2 = 1 << (N - 1).bit_length()
        x = x + [0] * (next_pow2 - N)
        N = next_pow2
    
    # Base case
    if N == 1:
        return x
    
    # Divide
    even = fft([x[i] for i in range(0, N, 2)])
    odd = fft([x[i] for i in range(1, N, 2)])
    
    # Conquer
    T = []
    for k in range(N // 2):
        t = complex(math.cos(-2 * math.pi * k / N), math.sin(-2 * math.pi * k / N)) * odd[k]
        T.append(t)
    
    return [even[k] + T[k] for k in range(N // 2)] + [even[k] - T[k] for k in range(N // 2)]

def find_dominant_frequencies(sample_rate, amplitudes):
    # Convert to complex numbers
    complex_data = [complex(amp, 0) for amp in amplitudes]
    
    # Perform FFT
    fft_result = fft(complex_data)
    
    # Calculate magnitudes
    magnitudes = [abs(val) for val in fft_result]
    
    # Only consider first half (positive frequencies)
    N = len(amplitudes)
    half_N = N // 2
    magnitudes = magnitudes[:half_N]
    
    # Calculate frequency bins
    freq_resolution = sample_rate / N
    frequencies = [i * freq_resolution for i in range(half_N)]
    
    # Find dominant frequency (excluding DC component at index 0)
    if len(magnitudes) > 1:
        max_idx = 1  # Start from index 1 to skip DC
        max_mag = magnitudes[1]
        
        for i in range(2, len(magnitudes)):
            if magnitudes[i] > max_mag:
                max_mag = magnitudes[i]
                max_idx = i
        
        dominant_freq = frequencies[max_idx]
        dominant_mag = max_mag
    else:
        dominant_freq = 0.0
        dominant_mag = 0.0
    
    return [dominant_freq], [round(dominant_mag, 2)]

def main():
    sample_rate, amplitudes = read_input()
    dominant_frequencies, magnitudes = find_dominant_frequencies(sample_rate, amplitudes)
    
    result = {
        "dominant_frequencies": dominant_frequencies,
        "magnitudes": magnitudes
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()