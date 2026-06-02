import sys, hashlib, json

def main():
    lines = sys.stdin.read().split('\n')
    index = int(lines[0].strip())
    timestamp = lines[1].strip()
    data = lines[2]
    previous_hash = lines[3].strip()
    content = str(index) + timestamp + data + previous_hash
    h = hashlib.sha256(content.encode('utf-8')).hexdigest()
    obj = {'index': index, 'timestamp': timestamp, 'data': data, 'previous_hash': previous_hash, 'hash': h}
    print(json.dumps(obj, separators=(',', ':')))

main()
