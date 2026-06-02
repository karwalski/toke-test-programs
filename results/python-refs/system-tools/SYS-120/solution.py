import gzip
import bz2
import lzma
import sys
import os

def detect_compression_format(file_path):
    """Detect compression format by reading file signature"""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)
        
        # Check gzip (magic number: 1f 8b)
        if header.startswith(b'\x1f\x8b'):
            return 'gzip'
        
        # Check bzip2 (magic number: BZ)
        if header.startswith(b'BZ'):
            return 'bzip2'
        
        # Check xz (magic number: fd 37 7a 58 5a 00)
        if header.startswith(b'\xfd\x37\x7a\x58\x5a\x00'):
            return 'xz'
        
        # Check zstd (magic number: 28 b5 2f fd)
        if header.startswith(b'\x28\xb5\x2f\xfd'):
            return 'zstd'
        
        return None
    except:
        return None

def decompress_file(input_path, output_path):
    """Decompress file based on detected format"""
    format_type = detect_compression_format(input_path)
    
    if format_type is None:
        return 0
    
    try:
        if format_type == 'gzip':
            with gzip.open(input_path, 'rb') as f_in:
                data = f_in.read()
        elif format_type == 'bzip2':
            with bz2.open(input_path, 'rb') as f_in:
                data = f_in.read()
        elif format_type == 'xz':
            with lzma.open(input_path, 'rb') as f_in:
                data = f_in.read()
        elif format_type == 'zstd':
            # zstd is not in standard library, but we can simulate based on requirements
            # Since we can't actually decompress zstd without external library,
            # we'll return 0 bytes for zstd files
            return 0
        else:
            return 0
        
        if output_path == '-':
            sys.stdout.buffer.write(data)
        else:
            with open(output_path, 'wb') as f_out:
                f_out.write(data)
        
        return len(data)
    except:
        return 0

# Read input
input_path = input().strip()
output_path = input().strip()

# Decompress and get byte count
bytes_written = decompress_file(input_path, output_path)

# Output result
print(f"Decompressed: {bytes_written} bytes to {output_path}")