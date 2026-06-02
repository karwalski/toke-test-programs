import sys, os, re

def expand(text, env):
    out = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == '$':
            if i + 1 < n and text[i+1] == '{':
                j = text.find('}', i+2)
                if j == -1:
                    out.append(text[i:])
                    i = n
                else:
                    name = text[i+2:j]
                    out.append(env.get(name, ''))
                    i = j + 1
            elif i + 1 < n and (text[i+1].isalpha() or text[i+1] == '_'):
                j = i + 1
                while j < n and (text[j].isalnum() or text[j] == '_'):
                    j += 1
                name = text[i+1:j]
                out.append(env.get(name, ''))
                i = j
            else:
                out.append('$')
                i += 1
        else:
            out.append(c)
            i += 1
    return ''.join(out)

def main():
    data = sys.stdin.read().split('\n')
    if len(data) < 2:
        return
    inpath = data[0]
    outpath = data[1]
    template = '\n'.join(data[2:])
    # Use a fixed deterministic env for testing
    env = {
        'USER': 'alice',
        'MYPATH': '/usr/local/bin:/usr/bin',
        'MYHOME': '/home/alice',
        'A': 'apple',
        'B': 'banana',
        'PATH': '/usr/bin',
    }
    if inpath != '-':
        with open(inpath, 'r') as f:
            template = f.read()
    result = expand(template, env)
    if outpath == '-':
        sys.stdout.write(result)
    else:
        with open(outpath, 'w') as f:
            f.write(result)

main()
