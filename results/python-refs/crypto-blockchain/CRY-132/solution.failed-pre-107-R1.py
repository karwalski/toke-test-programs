import sys

def main():
    # Read input
    r_hex = input().strip()
    s_hex = input().strip()
    n_hex = input().strip()
    
    # Convert hex to integers
    r = int(r_hex, 16)
    s = int(s_hex, 16)
    n = int(n_hex, 16)
    
    # Check malleability: s > n/2
    half_n = n // 2
    
    if s > half_n:
        # Malleable - normalize s
        normalized_s = n - s
        print(f"MALLEABLE (normalized s = {normalized_s:x})")
    else:
        # Canonical
        print("CANONICAL")

if __name__ == "__main__":
    main()