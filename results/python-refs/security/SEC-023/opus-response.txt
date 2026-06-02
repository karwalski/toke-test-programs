import json
import sys

def main():
    try:
        filepath = input().strip()
        language = input().strip()
    except EOFError:
        filepath = ""
        language = ""
    
    sys.stdout.write('[')

if __name__ == "__main__":
    main()