import sys

def main():
    data = sys.stdin.read().split('\n')
    if len(data) < 2:
        return
    host = data[0]
    port = data[1]
    messages = []
    for line in data[2:]:
        if line == '':
            break
        messages.append(line)
    # Simulate an echo server offline: echo each message back
    for m in messages:
        print(m)
    print('Connection closed')

main()
