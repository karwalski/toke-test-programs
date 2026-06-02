import platform
import socket
import os

def get_system_info():
    # Get OS name and version
    system = platform.system()
    if system == "Linux":
        try:
            with open('/etc/os-release', 'r') as f:
                lines = f.readlines()
                name = None
                version = None
                for line in lines:
                    if line.startswith('NAME='):
                        name = line.split('=')[1].strip().strip('"')
                    elif line.startswith('VERSION='):
                        version = line.split('=')[1].strip().strip('"')
                if name and version:
                    os_info = f"{name} {version}"
                else:
                    os_info = f"{system} {platform.release()}"
        except:
            os_info = f"{system} {platform.release()}"
    else:
        os_info = f"{system} {platform.release()}"
    
    # Get kernel version
    kernel_version = platform.release()
    
    # Get hostname
    hostname = socket.gethostname()
    
    # Get CPU count
    cpu_count = os.cpu_count()
    
    # Get total RAM in GB
    mem_gb = 0
    if system == "Linux":
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal:'):
                        mem_kb = int(line.split()[1])
                        mem_gb = round(mem_kb / (1024 * 1024))
                        break
        except:
            mem_gb = 0
    else:
        # For non-Linux systems, try to get memory info using platform-specific methods
        try:
            if system == "Darwin":  # macOS
                import subprocess
                result = subprocess.run(['sysctl', '-n', 'hw.memsize'], capture_output=True, text=True)
                if result.returncode == 0:
                    mem_bytes = int(result.stdout.strip())
                    mem_gb = round(mem_bytes / (1024**3))
            elif system == "Windows":
                import subprocess
                result = subprocess.run(['wmic', 'computersystem', 'get', 'TotalPhysicalMemory'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        mem_bytes = int(lines[1].strip())
                        mem_gb = round(mem_bytes / (1024**3))
        except:
            mem_gb = 0
    
    return os_info, kernel_version, hostname, cpu_count, mem_gb

# Read from stdin (but ignore as per requirement)
try:
    input()
except:
    pass

# Get system information
os_info, kernel_version, hostname, cpu_count, mem_gb = get_system_info()

# Output in the required format
print(f"OS: {os_info}")
print(f"Kernel: {kernel_version}")
print(f"Hostname: {hostname}")
print(f"CPUs: {cpu_count}")
print(f"RAM: {mem_gb} GB")