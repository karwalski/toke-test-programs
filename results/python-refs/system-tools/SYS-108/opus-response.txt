import sys

def main():
    try:
        s = input().strip()
    except EOFError:
        s = ''
    if s == 'LISTEN':
        print('(listening TCP sockets)')
    else:
        print('(all TCP connections)')

if __name__ == "__main__":
    main()