import sys

def get_magic_bytes(filepath):
    """Read the first few bytes of a file to determine its type"""
    try:
        with open(filepath, 'rb') as f:
            magic = f.read(16)  # Read first 16 bytes
            return magic
    except (IOError, OSError):
        return b''

def identify_file_type(filepath):
    """Identify file type based on magic bytes"""
    magic = get_magic_bytes(filepath)
    
    if not magic:
        return "cannot open"
    
    # Check for common file types based on magic bytes
    if magic.startswith(b'\x89PNG\r\n\x1a\n'):
        return "PNG image data"
    elif magic.startswith(b'\xff\xd8\xff'):
        return "JPEG image data"
    elif magic.startswith(b'GIF8'):
        return "GIF image data"
    elif magic.startswith(b'%PDF'):
        return "PDF document"
    elif magic.startswith(b'\x50\x4b\x03\x04') or magic.startswith(b'\x50\x4b\x05\x06') or magic.startswith(b'\x50\x4b\x07\x08'):
        return "Zip archive data"
    elif magic.startswith(b'\x7fELF'):
        return "ELF"
    elif magic.startswith(b'MZ'):
        return "PE32 executable"
    elif magic.startswith(b'\x1f\x8b'):
        return "gzip compressed data"
    elif magic.startswith(b'BM'):
        return "PC bitmap"
    elif magic.startswith(b'RIFF') and b'WAVE' in magic[:12]:
        return "WAVE audio"
    elif magic.startswith(b'\x00\x00\x01\x00') or magic.startswith(b'\x00\x00\x02\x00'):
        return "MS Windows icon resource"
    else:
        # Check if it's text by examining if all bytes are printable ASCII or common whitespace
        try:
            with open(filepath, 'rb') as f:
                sample = f.read(512)  # Read more for text detection
            
            if not sample:
                return "empty"
            
            # Check if it's ASCII text
            try:
                text_content = sample.decode('ascii')
                # Check if all characters are printable or whitespace
                if all(c.isprintable() or c in '\n\r\t' for c in text_content):
                    return "ASCII text"
            except UnicodeDecodeError:
                pass
            
            # Check if it's UTF-8 text
            try:
                sample.decode('utf-8')
                return "UTF-8 Unicode text"
            except UnicodeDecodeError:
                pass
            
        except (IOError, OSError):
            pass
        
        return "data"

def main():
    for line in sys.stdin:
        filepath = line.strip()
        if filepath:
            file_type = identify_file_type(filepath)
            print(f"{filepath}: {file_type}")

if __name__ == "__main__":
    main()