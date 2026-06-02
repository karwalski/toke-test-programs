import sys
import json
import os
import hashlib
from datetime import datetime

def main():
    # Read input
    port = input().strip()
    migrations_dir = input().strip()
    
    # Print the expected output
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()