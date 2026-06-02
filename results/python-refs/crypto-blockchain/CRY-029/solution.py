import sys
def main():
    data=sys.stdin.read().split()
    n=int(data[0],16)
    d=int(data[1],16)
    c=int(data[2],16)
    print(pow(c,d,n))
main()
