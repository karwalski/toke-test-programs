import sys
import json

def detect_hidden_chars():
    # Read all input from stdin
    text = sys.stdin.read()
    
    # Define zero-width characters
    ZWSP = '\u200B'  # Zero Width Space
    ZWNJ = '\u200C'  # Zero Width Non-Joiner
    ZWJ = '\u200D'   # Zero Width Joiner
    BOM = '\uFEFF'   # Byte Order Mark
    
    zero_width_chars = {ZWSP, ZWNJ, ZWJ, BOM}
    
    # Count characters
    total_chars = len(text)
    hidden_chars = sum(1 for char in text if char in zero_width_chars)
    visible_chars = total_chars - hidden_chars
    
    # Extract hidden character sequence
    hidden_sequence = ''.join(char for char in text if char in zero_width_chars)
    
    # Try to decode as binary (common encoding method)
    hidden_bits = ""
    decoded_data = ""
    possible_encoding = "none"
    
    if hidden_chars > 0:
        # Convert to binary representation (simple mapping)
        char_to_bit = {
            ZWSP: '0',
            ZWNJ: '1',
            ZWJ: '0',
            BOM: '1'
        }
        
        hidden_bits = ''.join(char_to_bit.get(char, '') for char in hidden_sequence)
        
        # Try to decode binary as ASCII
        if len(hidden_bits) >= 8 and len(hidden_bits) % 8 == 0:
            try:
                decoded_bytes = []
                for i in range(0, len(hidden_bits), 8):
                    byte_str = hidden_bits[i:i+8]
                    byte_val = int(byte_str, 2)
                    if 32 <= byte_val <= 126:  # Printable ASCII
                        decoded_bytes.append(chr(byte_val))
                    else:
                        decoded_bytes = []
                        break
                
                if decoded_bytes:
                    decoded_data = ''.join(decoded_bytes)
                    possible_encoding = "binary"
            except:
                pass
        
        if not decoded_data and hidden_chars > 0:
            possible_encoding = "unknown"
    
    # Create output
    result = {
        "totalChars": total_chars,
        "visibleChars": visible_chars,
        "hiddenChars": hidden_chars,
        "hiddenBits": hidden_bits,
        "possibleEncoding": possible_encoding,
        "decodedData": decoded_data
    }
    
    print(json.dumps(result))

if __name__ == "__main__":
    detect_hidden_chars()