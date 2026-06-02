import sys

def main():
    # Read input
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            lines.append(line)
    
    # Parse matrix
    matrix = []
    for line in lines:
        row = [int(x) for x in line.split()]
        matrix.append(row)
    
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    
    # Convert to CSR format
    values = []
    col_indices = []
    row_pointers = [0]
    
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] != 0:
                values.append(matrix[i][j])
                col_indices.append(j)
        row_pointers.append(len(values))
    
    # Calculate compression ratio
    total_elements = rows * cols
    non_zero_elements = len(values)
    csr_storage = len(values) + len(col_indices) + len(row_pointers)
    compression_ratio = (1 - csr_storage / total_elements) * 100
    
    # Output results
    print(f"Values: {values}")
    print(f"Col indices: {col_indices}")
    print(f"Row pointers: {row_pointers}")
    print(f"Compression: {compression_ratio}%")

if __name__ == "__main__":
    main()