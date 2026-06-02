import sys

def detect_mime_type(hex_string):
    # Convert hex string to bytes
    try:
        data = bytes.fromhex(hex_string)
    except ValueError:
        return "application/octet-stream - Unknown binary file"
    
    # Magic byte signatures
    signatures = [
        # JPEG
        (b'\xFF\xD8\xFF\xE0', "image/jpeg - JPEG image"),
        (b'\xFF\xD8\xFF\xE1', "image/jpeg - JPEG image"),
        (b'\xFF\xD8\xFF\xE2', "image/jpeg - JPEG image"),
        (b'\xFF\xD8\xFF\xE3', "image/jpeg - JPEG image"),
        (b'\xFF\xD8\xFF\xE8', "image/jpeg - JPEG image"),
        (b'\xFF\xD8\xFF\xDB', "image/jpeg - JPEG image"),
        (b'\xFF\xD8\xFF\xEE', "image/jpeg - JPEG image"),
        # PNG
        (b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', "image/png - PNG image"),
        # GIF
        (b'GIF87a', "image/gif - GIF image"),
        (b'GIF89a', "image/gif - GIF image"),
        # PDF
        (b'%PDF', "application/pdf - PDF document"),
        # ZIP
        (b'PK\x03\x04', "application/zip - ZIP archive"),
        (b'PK\x05\x06', "application/zip - ZIP archive"),
        (b'PK\x07\x08', "application/zip - ZIP archive"),
        # RAR
        (b'Rar!\x1A\x07\x00', "application/x-rar-compressed - RAR archive"),
        (b'Rar!\x1A\x07\x01\x00', "application/x-rar-compressed - RAR archive"),
        # 7z
        (b'7z\xBC\xAF\x27\x1C', "application/x-7z-compressed - 7-Zip archive"),
        # BMP
        (b'BM', "image/bmp - BMP image"),
        # TIFF
        (b'II\x2A\x00', "image/tiff - TIFF image"),
        (b'MM\x00\x2A', "image/tiff - TIFF image"),
        # WebP
        (b'RIFF', "image/webp - WebP image"),
        # MP3
        (b'ID3', "audio/mpeg - MP3 audio"),
        (b'\xFF\xFB', "audio/mpeg - MP3 audio"),
        # WAV
        (b'RIFF', "audio/wav - WAV audio"),
        # AVI
        (b'RIFF', "video/x-msvideo - AVI video"),
        # MP4
        (b'\x00\x00\x00\x18ftypmp4', "video/mp4 - MP4 video"),
        (b'\x00\x00\x00\x1Cftypmp4', "video/mp4 - MP4 video"),
        (b'\x00\x00\x00\x20ftypmp4', "video/mp4 - MP4 video"),
        # EXE
        (b'MZ', "application/x-msdownload - Windows executable"),
        # ELF
        (b'\x7FELF', "application/x-executable - Linux executable"),
    ]
    
    # Check signatures
    for signature, mime_type in signatures:
        if data.startswith(signature):
            return mime_type
    
    return "application/octet-stream - Unknown binary file"

# Read hex string from stdin
hex_input = sys.stdin.read().strip()
result = detect_mime_type(hex_input)
print(result)