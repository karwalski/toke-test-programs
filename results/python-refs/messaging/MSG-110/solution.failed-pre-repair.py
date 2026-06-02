import json
import time
import random
import secrets
from hashlib import sha256
import hmac

def simulate_aes_256_gcm_encrypt(data):
    """Simulate AES-256-GCM encryption"""
    # Simulate key derivation and encryption overhead
    key = secrets.token_bytes(32)
    iv = secrets.token_bytes(12)
    
    # Simulate block cipher operations
    blocks = len(data) // 16 + (1 if len(data) % 16 else 0)
    
    # Simple simulation: XOR with key-derived stream
    result = bytearray()
    for i in range(len(data)):
        key_byte = key[i % 32]
        result.append(data[i] ^ key_byte)
    
    # Simulate GCM authentication tag
    tag = hmac.new(key, bytes(result), sha256).digest()[:16]
    
    return bytes(result) + tag

def simulate_chacha20_poly1305_encrypt(data):
    """Simulate ChaCha20-Poly1305 encryption"""
    # Simulate key and nonce
    key = secrets.token_bytes(32)
    nonce = secrets.token_bytes(12)
    
    # Simple stream cipher simulation
    result = bytearray()
    for i in range(len(data)):
        # Simulate ChaCha20 keystream generation
        stream_byte = (key[i % 32] + nonce[i % 12] + i) % 256
        result.append(data[i] ^ stream_byte)
    
    # Simulate Poly1305 MAC
    mac_key = key[:16]
    mac = hmac.new(mac_key, bytes(result), sha256).digest()[:16]
    
    return bytes(result) + mac

def benchmark_encryption(algorithm, data, iterations):
    """Benchmark encryption algorithm"""
    latencies = []
    
    if algorithm == "AES-256-GCM":
        encrypt_func = simulate_aes_256_gcm_encrypt
    elif algorithm == "ChaCha20-Poly1305":
        encrypt_func = simulate_chacha20_poly1305_encrypt
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    
    # Warmup
    for _ in range(10):
        encrypt_func(data)
    
    # Actual benchmark
    start_time = time.perf_counter()
    
    for _ in range(iterations):
        iter_start = time.perf_counter()
        encrypt_func(data)
        iter_end = time.perf_counter()
        latencies.append((iter_end - iter_start) * 1_000_000)  # Convert to microseconds
    
    end_time = time.perf_counter()
    
    total_time = end_time - start_time
    total_bytes = len(data) * iterations
    throughput_mbps = (total_bytes / (1024 * 1024)) / total_time
    
    latencies.sort()
    p50 = latencies[len(latencies) // 2]
    p99 = latencies[int(len(latencies) * 0.99)]
    
    return throughput_mbps, p50, p99

def format_throughput(mbps):
    """Format throughput for display"""
    if mbps >= 1024:
        return f"{mbps/1024:.1f}GB/s"
    else:
        return f"{int(mbps)}MB/s"

def format_size(size_bytes):
    """Format size for display"""
    if size_bytes >= 1024:
        return f"{size_bytes//1024}KB"
    else:
        return f"{size_bytes}B"

def format_latency(latency_us):
    """Format latency for display"""
    if latency_us >= 1:
        return f"{latency_us:.1f}us"
    else:
        return f"{latency_us:.1f}us"

# Read input
algorithms = json.loads(input().strip())
sizes = json.loads(input().strip())
iterations = int(input().strip())

# Run benchmarks
results = {}
latency_results = {}

for algorithm in algorithms:
    results[algorithm] = {}
    latency_results[algorithm] = {}
    
    for size in sizes:
        # Generate test data
        test_data = secrets.token_bytes(size)
        
        # Run benchmark
        throughput, p50, p99 = benchmark_encryption(algorithm, test_data, iterations)
        
        results[algorithm][size] = throughput
        latency_results[algorithm][size] = (p50, p99)

# Format and print results
print("| Algorithm          |  64B    |  1KB    |  64KB   |")

for algorithm in algorithms:
    row = f"| {algorithm:<18} |"
    for size in sizes:
        throughput = results[algorithm][size]
        formatted = format_throughput(throughput)
        row += f" {formatted:>7} |"
    print(row)

print("latency (p50/p99):")
for algorithm in algorithms:
    latency_parts = []
    for size in sizes:
        p50, p99 = latency_results[algorithm][size]
        size_str = format_size(size)
        latency_str = f"{format_latency(p50)}/{format_latency(p99)} ({size_str})"
        latency_parts.append(latency_str)
    
    print(f"  {algorithm}: {', '.join(latency_parts)}")