import sys
import time
import random

def get_mock_interface_stats():
    """Generate mock network interface statistics"""
    interfaces = ['eth0', 'wlan0', 'lo']
    stats = {}
    for iface in interfaces:
        # Generate random bytes values (simulating /proc/net/dev data)
        rx_bytes = random.randint(1000000, 100000000)
        tx_bytes = random.randint(1000000, 100000000)
        stats[iface] = {'rx_bytes': rx_bytes, 'tx_bytes': tx_bytes}
    return stats

def main():
    # Read input
    interval_seconds = int(input().strip())
    samples = int(input().strip())
    
    # Initialize with first measurement
    prev_stats = get_mock_interface_stats()
    
    for sample in range(samples):
        if sample > 0:
            # Wait for the interval (but not for first sample)
            time.sleep(interval_seconds)
        
        # Get current stats
        curr_stats = get_mock_interface_stats()
        
        if sample > 0:  # Skip first sample since we need delta
            # Calculate and display rates for each interface
            for iface in sorted(curr_stats.keys()):
                if iface in prev_stats:
                    # Calculate bytes per second
                    rx_delta = curr_stats[iface]['rx_bytes'] - prev_stats[iface]['rx_bytes']
                    tx_delta = curr_stats[iface]['tx_bytes'] - prev_stats[iface]['tx_bytes']
                    
                    rx_mbps = (rx_delta / interval_seconds) / (1024 * 1024)
                    tx_mbps = (tx_delta / interval_seconds) / (1024 * 1024)
                    
                    print(f"{iface}: rx={rx_mbps:.2f} MB/s tx={tx_mbps:.2f} MB/s")
        
        # Update previous stats
        prev_stats = curr_stats.copy()

if __name__ == "__main__":
    main()