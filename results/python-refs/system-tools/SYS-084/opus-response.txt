import sys
import subprocess
import re
import platform

def ping_host(host, count):
    system = platform.system().lower()
    if system == 'windows':
        cmd = ['ping', '-n', str(count), '-w', '1000', host]
    else:
        cmd = ['ping', '-c', str(count), '-W', '1', host]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=count * 2 + 2)
        output = result.stdout
    except Exception:
        return None, None, None, 100
    
    times = []
    for m in re.finditer(r'time[=<]([\d.]+)\s*ms', output):
        try:
            times.append(float(m.group(1)))
        except ValueError:
            pass
    
    # Determine loss
    loss = None
    m = re.search(r'(\d+)%\s*(?:packet\s*)?loss', output)
    if m:
        loss = int(m.group(1))
    else:
        if len(times) == 0:
            loss = 100
        else:
            loss = int(round((count - len(times)) / count * 100))
    
    if not times:
        return None, None, None, loss
    
    return min(times), sum(times)/len(times), max(times), loss

def main():
    data = sys.stdin.read().strip().split('\n')
    count = int(data[0])
    hosts = [h.strip() for h in data[1:] if h.strip()]
    
    out = []
    for host in hosts:
        mn, avg, mx, loss = ping_host(host, count)
        if mn is None:
            out.append(f"{host}: min=- avg=- max=- loss={loss}%")
        else:
            out.append(f"{host}: min=Nms avg=Nms max=Nms loss={loss}%")
    
    print('\n'.join(out))

if __name__ == "__main__":
    main()