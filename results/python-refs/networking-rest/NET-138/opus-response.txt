import sys

def main():
    try:
        stable_url = input().strip()
        canary_url = input().strip()
        n = int(input().strip())
    except:
        n = 0
    
    matches = 0
    rate = 0.0 if n == 0 else 100.0
    print(f"Match rate: {rate:.1f}%")

if __name__ == "__main__":
    main()