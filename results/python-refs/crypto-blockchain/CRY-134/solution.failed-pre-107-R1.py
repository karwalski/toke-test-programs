import json
import hashlib
import sys

def hash_element(element):
    """Hash an element to get a position in the filter"""
    return int(hashlib.sha256(element.encode()).hexdigest(), 16)

def golomb_encode(value, m):
    """Encode a value using Golomb coding with parameter m"""
    q = value // m
    r = value % m
    
    # Unary encode q (q ones followed by a zero)
    unary = '1' * q + '0'
    
    # Binary encode r with ceil(log2(m)) bits
    if m == 1:
        return unary
    
    b = (m - 1).bit_length()
    binary = format(r, f'0{b}b')
    
    return unary + binary

def create_golomb_filter(elements, m=8):
    """Create a Golomb-coded set filter"""
    if not elements:
        return ""
    
    # Hash all elements and sort the positions
    positions = []
    for element in elements:
        pos = hash_element(element) % (1 << 20)  # Use 20-bit positions
        positions.append(pos)
    
    positions.sort()
    
    # Encode differences between consecutive positions
    filter_bits = ""
    prev = 0
    
    for pos in positions:
        diff = pos - prev
        filter_bits += golomb_encode(diff, m)
        prev = pos
    
    # Pad to byte boundary
    while len(filter_bits) % 8 != 0:
        filter_bits += '0'
    
    # Convert to hex
    hex_result = ""
    for i in range(0, len(filter_bits), 8):
        byte = filter_bits[i:i+8]
        hex_result += format(int(byte, 2), '02x')
    
    return hex_result

def golomb_decode(bits, m):
    """Decode a Golomb-encoded value"""
    pos = 0
    
    # Decode unary part (count ones until zero)
    q = 0
    while pos < len(bits) and bits[pos] == '1':
        q += 1
        pos += 1
    
    if pos >= len(bits):
        return None, pos
    
    # Skip the zero
    pos += 1
    
    # Decode binary part
    if m == 1:
        return q, pos
    
    b = (m - 1).bit_length()
    if pos + b > len(bits):
        return None, pos
    
    r = int(bits[pos:pos+b], 2)
    pos += b
    
    return q * m + r, pos

def test_membership(filter_hex, query, m=8):
    """Test if query is in the Golomb filter"""
    if not filter_hex:
        return False
    
    # Convert hex back to bits
    filter_bits = ""
    for i in range(0, len(filter_hex), 2):
        byte_hex = filter_hex[i:i+2]
        filter_bits += format(int(byte_hex, 16), '08b')
    
    # Hash the query
    query_pos = hash_element(query) % (1 << 20)
    
    # Decode the filter and check positions
    pos = 0
    current_pos = 0
    
    while pos < len(filter_bits):
        diff, new_pos = golomb_decode(filter_bits[pos:], m)
        if diff is None:
            break
        
        current_pos += diff
        if current_pos == query_pos:
            return True
        if current_pos > query_pos:
            return False
        
        pos += new_pos
    
    return False

# Read input
line1 = input().strip()
line2 = input().strip()

# Parse elements
elements = json.loads(line1)
query = line2

# Create filter
filter_hex = create_golomb_filter(elements)

# Test membership
is_match = test_membership(filter_hex, query)

# Output
print(filter_hex)
print("MATCH" if is_match else "NO_MATCH")