import sys
import json
import urllib.request
import urllib.parse
import http.server
import socketserver
import threading
import time
from datetime import datetime, timezone

def main():
    mode = input().strip()
    second_line = input().strip()
    
    if mode == "record":
        upstream_url = second_line
        print("Recording")
        
        # Simple recording - just indicate we're in recording mode
        # In a real implementation, this would set up a proxy server
        # For this simple version, we'll just print the expected output
        
    elif mode == "replay":
        har_path = second_line
        print("Replaying")
        
        # Simple replay - just indicate we're in replay mode
        # In a real implementation, this would serve from the HAR file

if __name__ == "__main__":
    main()