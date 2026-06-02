import sys
import time

def main():
    # Read API key
    api_key = input().strip()
    
    # Read URLs
    urls = []
    while True:
        try:
            line = input().strip()
            if not line:
                break
            urls.append(line)
        except EOFError:
            break
    
    # Process only the first URL
    if urls:
        print(urls[0])

if __name__ == "__main__":
    main()