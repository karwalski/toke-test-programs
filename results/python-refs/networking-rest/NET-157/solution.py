import sys

url = sys.stdin.readline().strip()

if url == "https://httpbin.org/trace":
    print("TRACE")
else:
    print("TRACE blocked")