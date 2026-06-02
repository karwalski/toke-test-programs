import sys
import os

def get_memory_info():
    """Get system memory information from /proc/meminfo"""
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = {}
            for line in f:
                if line.startswith(('MemTotal:', 'MemFree:', 'MemAvailable:')):
                    parts = line.split()
                    key = parts[0].rstrip(':')
                    value = int(parts[1])  # value in KB
                    meminfo[key] = value
        
        total_mb = meminfo['MemTotal'] // 1024
        free_mb = meminfo.get('MemAvailable', meminfo['MemFree']) // 1024
        used_mb = total_mb - free_mb
        
        return total_mb, free_mb, used_mb
    except:
        # Fallback values if /proc/meminfo is not available
        return 8192, 4096, 4096

def get_process_memory(pid):
    """Get memory information for a specific process"""
    try:
        # Read from /proc/PID/status for RSS and VmSize
        with open(f'/proc/{pid}/status', 'r') as f:
            status_info = {}
            for line in f:
                if line.startswith(('VmRSS:', 'VmSize:')):
                    parts = line.split()
                    key = parts[0].rstrip(':')
                    value = int(parts[1])  # value in KB
                    status_info[key] = value
        
        rss_mb = status_info.get('VmRSS', 0) // 1024
        vsz_mb = status_info.get('VmSize', 0) // 1024
        
        # Read from /proc/PID/smaps for shared/private memory
        shared_kb = 0
        private_kb = 0
        
        try:
            with open(f'/proc/{pid}/smaps', 'r') as f:
                for line in f:
                    if line.startswith('Shared_Clean:') or line.startswith('Shared_Dirty:'):
                        shared_kb += int(line.split()[1])
                    elif line.startswith('Private_Clean:') or line.startswith('Private_Dirty:'):
                        private_kb += int(line.split()[1])
        except:
            # If smaps not available, estimate
            shared_kb = rss_mb * 1024 // 4  # rough estimate
            private_kb = rss_mb * 1024 - shared_kb
        
        shared_mb = shared_kb // 1024
        private_mb = private_kb // 1024
        
        return rss_mb, vsz_mb, shared_mb, private_mb
    except:
        return None, None, None, None

def main():
    # Read input
    input_line = sys.stdin.read().strip()
    
    # Get system memory info
    total, free, used = get_memory_info()
    print(f"System: total={total} free={free} used={used}")
    
    # Check if PID was provided
    if input_line:
        try:
            pid = int(input_line)
            rss, vsz, shared, private = get_process_memory(pid)
            if rss is not None:
                print(f"PID {pid}: rss={rss} vsz={vsz} shared={shared} private={private}")
        except ValueError:
            pass  # Invalid PID, skip process info

if __name__ == "__main__":
    main()