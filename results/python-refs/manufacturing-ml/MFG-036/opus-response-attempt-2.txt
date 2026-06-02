import sys
import json
import math

def main():
    data = sys.stdin.read().strip().split('\n')
    sample_rate = int(data[0].split(',')[1])
    amplitudes = [float(x) for x in data[1].split(',')]
    
    N = len(amplitudes)
    # DFT
    fft_result = []
    for k in range(N):
        s = 0+0j
        for n in range(N):
            angle = -2 * math.pi * k * n / N
            s += amplitudes[n] * complex(math.cos(angle), math.sin(angle))
        fft_result.append(s)
    
    half_N = N // 2
    mags = []
    for k in range(half_N + 1):
        m = abs(fft_result[k]) * 2 / N
        mags.append(m)
    
    freqs = [k * sample_rate / N for k in range(half_N + 1)]
    
    search_mags = mags[1:]
    max_mag = max(search_mags)
    threshold = 0.1 * max_mag
    
    dom_freqs = []
    dom_mags = []
    for i in range(1, len(mags)):
        if mags[i] > threshold:
            dom_freqs.append(round(freqs[i], 2))
            dom_mags.append(round(mags[i], 2))
    
    result = {"dominant_frequencies": dom_freqs, "magnitudes": dom_mags}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()