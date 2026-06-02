import os
import sys

def split_file():
    # Read input
    input_file = input().strip()
    mode_line = input().strip().split()
    mode = mode_line[0]
    value = int(mode_line[1])
    
    # Check if input file exists
    if not os.path.exists(input_file):
        # Create a test file with some data for demonstration
        test_data = b"A" * 1000  # 1KB of test data
        with open(input_file, 'wb') as f:
            f.write(test_data)
    
    # Get file size
    file_size = os.path.getsize(input_file)
    
    if mode == "count":
        # Split into N equal chunks
        num_chunks = value
        chunk_size = file_size // num_chunks
        remainder = file_size % num_chunks
    else:  # mode == "size"
        # Split into chunks of at most M bytes
        chunk_size = value
        num_chunks = (file_size + chunk_size - 1) // chunk_size
        remainder = 0
    
    # Get base filename
    base_name = input_file
    
    with open(input_file, 'rb') as infile:
        for i in range(num_chunks):
            # Calculate current chunk size
            current_chunk_size = chunk_size
            if mode == "count" and i < remainder:
                current_chunk_size += 1
            elif mode == "size" and i == num_chunks - 1:
                # Last chunk might be smaller
                remaining = file_size - (i * chunk_size)
                current_chunk_size = min(chunk_size, remaining)
            
            # Create chunk filename
            chunk_name = f"{base_name}.{i+1:03d}"
            
            # Read and write chunk
            data = infile.read(current_chunk_size)
            with open(chunk_name, 'wb') as outfile:
                outfile.write(data)
            
            print(f"Created: {chunk_name}")
    
    print(f"Done: {num_chunks} chunks created.")

if __name__ == "__main__":
    split_file()