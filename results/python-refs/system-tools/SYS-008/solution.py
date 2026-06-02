import sys
import subprocess

def is_process_running(process_name):
    try:
        # Use ps command to check if process is running
        result = subprocess.run(['ps', '-A'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            processes = result.stdout.lower()
            return process_name.lower() in processes
        else:
            # If ps command fails, try pgrep as fallback
            result = subprocess.run(['pgrep', process_name], capture_output=True, timeout=5)
            return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # If commands fail or timeout, assume process is not running
        return False

# Read service names from stdin
for line in sys.stdin:
    service_name = line.strip()
    if service_name:  # Skip empty lines
        if is_process_running(service_name):
            print(f"{service_name}: RUNNING")
        else:
            print(f"{service_name}: STOPPED")