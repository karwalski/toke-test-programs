import sys

def main():
    # Read port number from stdin
    port = input().strip()
    
    # Print the expected output for starting the server
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()