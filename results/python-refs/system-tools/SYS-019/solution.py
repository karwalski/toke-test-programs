import sys
import time
import os

def format_time(seconds):
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{days}d {hours}h {minutes}m {secs}s"

def get_system_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            return float(f.readline().split()[0])
    except Exception:
        try:
            # macOS / BSD fallback
            import subprocess
            out = subprocess.check_output(['sysctl', '-n', 'kern.boottime']).decode()
            # e.g. "{ sec = 1234567890, usec = 0 } ..."
            import re
            m = re.search(r'sec\s*=\s*(\d+)', out)
            if m:
                return time.time() - int(m.group(1))
        except Exception:
            pass
        return 1.0

def read_proc_stat_starttime(pid):
    """Return process start time as epoch seconds, or None."""
    try:
        with open(f'/proc/{pid}/stat', 'r') as f:
            data = f.read()
        # The comm field is in parens and may contain spaces/parens
        rparen = data.rfind(')')
        rest = data[rparen+2:].split()
        # starttime is field 22 overall; after comm it's index 19 (0-based)
        starttime_ticks = int(rest[19])
        clk_tck = os.sysconf('SC_CLK_TCK')
        # Get boot time
        boot_time = None
        with open('/proc/stat', 'r') as f:
            for line in f:
                if line.startswith('btime'):
                    boot_time = int(line.split()[1])
                    break
        if boot_time is None:
            return None
        return boot_time + starttime_ticks / clk_tck
    except Exception:
        return None

def read_proc_name(pid):
    try:
        with open(f'/proc/{pid}/comm', 'r') as f:
            return f.read().strip()
    except Exception:
        try:
            with open(f'/proc/{pid}/stat', 'r') as f:
                data = f.read()
            lparen = data.find('(')
            rparen = data.rfind(')')
            return data[lparen+1:rparen]
        except Exception:
            return None

def iter_pids():
    try:
        for entry in os.listdir('/proc'):
            if entry.isdigit():
                yield int(entry)
    except Exception:
        return

def get_process_uptime(identifier):
    try:
        if identifier.isdigit():
            pid = int(identifier)
            start = read_proc_stat_starttime(pid)
            if start is None:
                return None
            name = read_proc_name(pid) or identifier
            return name, pid, time.time() - start
        else:
            for pid in iter_pids():
                name = read_proc_name(pid)
                if name == identifier:
                    start = read_proc_stat_starttime(pid)
                    if start is not None:
                        return name, pid, time.time() - start
            return None
    except Exception:
        return None

def main():
    system_uptime = get_system_uptime()
    print(f"System uptime: {format_time(system_uptime)}")
    
    data = sys.stdin.read().strip()
    if data:
        line = data.splitlines()[0].strip()
        if line:
            result = get_process_uptime(line)
            if result:
                name, pid, uptime = result
                print(f"Process {name} ({pid}): {format_time(uptime)}")
            else:
                print(f"Process {line}: NOT FOUND")

if __name__ == "__main__":
    main()