import sys
import time

def main():
    # Read the rate from the first line
    rate_line = sys.stdin.readline().strip()
    rate_bytes_per_second = int(rate_line)
    
    # Read all remaining data
    remaining_data = sys.stdin.read()
    
    # Calculate delay per byte
    delay_per_byte = 1.0 / rate_bytes_per_second if rate_bytes_per_second > 0 else 0
    
    # Output data byte by byte with throttling
    start_time = time.time()
    bytes_written = 0
    
    for byte in remaining_data.encode('utf-8'):
        # Write the byte
        sys.stdout.buffer.write(bytes([byte]))
        sys.stdout.buffer.flush()
        bytes_written += 1
        
        # Calculate expected time for this many bytes
        expected_time = bytes_written * delay_per_byte
        elapsed_time = time.time() - start_time
        
        # Sleep if we're going too fast
        if elapsed_time < expected_time:
            sleep_time = expected_time - elapsed_time
            # Limit sleep to avoid exceeding 10 second total runtime
            if time.time() - start_time + sleep_time < 9.5:
                time.sleep(sleep_time)

if __name__ == "__main__":
    main()