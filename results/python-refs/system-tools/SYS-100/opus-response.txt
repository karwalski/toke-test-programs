#!/usr/bin/env python3
import os
import glob
import sys

def read_file(path):
    with open(path, 'r') as f:
        return f.read().strip()

def try_cpufreq():
    cpu_dirs = glob.glob('/sys/devices/system/cpu/cpu[0-9]*/cpufreq')
    if not cpu_dirs:
        return False
    cpu_dirs.sort(key=lambda x: int(x.split('cpu')[-1].split('/')[0]))
    printed = False
    for cpu_dir in cpu_dirs:
        try:
            core_num = int(cpu_dir.split('cpu')[-1].split('/')[0])
            try:
                cur = int(read_file(os.path.join(cpu_dir, 'scaling_cur_freq'))) // 1000
            except Exception:
                try:
                    cur = int(read_file(os.path.join(cpu_dir, 'cpuinfo_cur_freq'))) // 1000
                except Exception:
                    cur = 0
            try:
                mn = int(read_file(os.path.join(cpu_dir, 'scaling_min_freq'))) // 1000
            except Exception:
                mn = int(read_file(os.path.join(cpu_dir, 'cpuinfo_min_freq'))) // 1000
            try:
                mx = int(read_file(os.path.join(cpu_dir, 'scaling_max_freq'))) // 1000
            except Exception:
                mx = int(read_file(os.path.join(cpu_dir, 'cpuinfo_max_freq'))) // 1000
            try:
                gov = read_file(os.path.join(cpu_dir, 'scaling_governor'))
            except Exception:
                gov = "unknown"
            print(f"Core {core_num}: cur={cur}MHz min={mn}MHz max={mx}MHz governor={gov}")
            printed = True
        except Exception:
            continue
    return printed

def try_cpuinfo():
    # Fallback: parse /proc/cpuinfo
    try:
        with open('/proc/cpuinfo', 'r') as f:
            data = f.read()
    except Exception:
        return False
    cores = []
    cur_mhz = None
    proc_id = None
    for line in data.splitlines():
        if ':' not in line:
            if proc_id is not None:
                cores.append((proc_id, cur_mhz))
                proc_id = None
                cur_mhz = None
            continue
        key, _, val = line.partition(':')
        key = key.strip()
        val = val.strip()
        if key == 'processor':
            try:
                proc_id = int(val)
            except Exception:
                proc_id = None
        elif key == 'cpu MHz':
            try:
                cur_mhz = int(float(val))
            except Exception:
                cur_mhz = 0
    if proc_id is not None:
        cores.append((proc_id, cur_mhz))
    if not cores:
        return False
    for pid, mhz in cores:
        if mhz is None:
            mhz = 0
        print(f"Core {pid}: cur={mhz}MHz min={mhz}MHz max={mhz}MHz governor=unknown")
    return True

def try_macos():
    import subprocess
    try:
        out = subprocess.check_output(['sysctl', '-n', 'hw.cpufrequency'], stderr=subprocess.DEVNULL).decode().strip()
        hz = int(out)
        mhz = hz // 1_000_000
    except Exception:
        try:
            out = subprocess.check_output(['sysctl', '-n', 'hw.cpufrequency_max'], stderr=subprocess.DEVNULL).decode().strip()
            mhz = int(out) // 1_000_000
        except Exception:
            mhz = 0
    try:
        ncpu = int(subprocess.check_output(['sysctl', '-n', 'hw.ncpu'], stderr=subprocess.DEVNULL).decode().strip())
    except Exception:
        ncpu = os.cpu_count() or 1
    for i in range(ncpu):
        print(f"Core {i}: cur={mhz}MHz min={mhz}MHz max={mhz}MHz governor=unknown")
    return True

def main():
    try:
        sys.stdin.read()
    except Exception:
        pass
    if sys.platform.startswith('linux'):
        if try_cpufreq():
            return
        if try_cpuinfo():
            return
        # last resort
        n = os.cpu_count() or 1
        for i in range(n):
            print(f"Core {i}: cur=0MHz min=0MHz max=0MHz governor=unknown")
    elif sys.platform == 'darwin':
        try_macos()
    else:
        n = os.cpu_count() or 1
        for i in range(n):
            print(f"Core {i}: cur=0MHz min=0MHz max=0MHz governor=unknown")

if __name__ == "__main__":
    main()