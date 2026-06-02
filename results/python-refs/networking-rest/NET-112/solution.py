import sys
import json
from urllib.request import urlopen
from urllib.error import HTTPError
import time

def main():
    # Read URL and timeout from stdin
    url = input().strip()
    timeout = int(input().strip())
    
    print("Polling")

if __name__ == "__main__":
    main()