import sys
import urllib.request
import urllib.parse
import os
import time

def download_with_progress(url, filepath):
    try:
        # Open the URL
        response = urllib.request.urlopen(url)
        
        # Get file size if available
        content_length = response.headers.get('Content-Length')
        total_size = int(content_length) if content_length else None
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        downloaded = 0
        chunk_size = 8192
        start_time = time.time()
        
        with open(filepath, 'wb') as f:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                
                f.write(chunk)
                downloaded += len(chunk)
                
                # Calculate progress
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    speed = downloaded / elapsed_time
                else:
                    speed = 0
                
                if total_size:
                    percentage = (downloaded / total_size) * 100
                    print(f"\r{percentage:.1f}% - {downloaded} bytes - {speed:.1f} bytes/s", 
                          file=sys.stderr, end='', flush=True)
                else:
                    print(f"\r{downloaded} bytes - {speed:.1f} bytes/s", 
                          file=sys.stderr, end='', flush=True)
        
        print("", file=sys.stderr)  # New line after progress
        print("Downloaded")
        
    except Exception as e:
        print(f"Error downloading file: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # Read URL and filepath from stdin
    url = input().strip()
    filepath = input().strip()
    
    download_with_progress(url, filepath)

if __name__ == "__main__":
    main()