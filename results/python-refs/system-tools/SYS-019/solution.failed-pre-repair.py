import sys
import time
import os
import psutil

def format_time(seconds):
    """Format seconds into days, hours, minutes, seconds"""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{days}d {hours}h {minutes}m {secs}s"

def get_system_uptime():
    """Get system uptime in seconds"""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            return uptime_seconds
    except:
        # Fallback for non-Linux systems
        return time.time() - psutil.boot_time()

def get_process_uptime(identifier):
    """Get process uptime by PID or name"""
    try:
        # Check if identifier is a PID (numeric)
        if identifier.isdigit():
            pid = int(identifier)
            try:
                proc = psutil.Process(pid)
                create_time = proc.create_time()
                uptime = time.time() - create_time
                return proc.name(), pid, uptime
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return None
        else:
            # Search by process name
            for proc in psutil.process_iter(['pid', 'name', 'create_time']):
                try:
                    if proc.info['name'] == identifier:
                        create_time = proc.info['create_time']
                        uptime = time.time() - create_time
                        return identifier, proc.info['pid'], uptime
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return None
    except:
        return None

def main():
    # Get system uptime
    system_uptime = get_system_uptime()
    print(f"System uptime: {format_time(system_uptime)}")
    
    # Read optional process identifier from stdin
    try:
        line = input().strip()
        if line:
            result = get_process_uptime(line)
            if result:
                name, pid, uptime = result
                print(f"Process {name} ({pid}): {format_time(uptime)}")
            else:
                print("NOT FOUND")
    except EOFError:
        # No input provided, only show system uptime
        pass

if __name__ == "__main__":
    main()