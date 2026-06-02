import sys
import subprocess
import json

def get_systemd_status(unit_name):
    try:
        # Use systemctl show to get detailed information about the unit
        result = subprocess.run(
            ['systemctl', 'show', unit_name, '--property=ActiveState,SubState,MainPID'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return "inactive", "dead", "-"
        
        # Parse the output
        active_state = "inactive"
        sub_state = "dead"
        main_pid = "-"
        
        for line in result.stdout.strip().split('\n'):
            if line.startswith('ActiveState='):
                active_state = line.split('=', 1)[1]
            elif line.startswith('SubState='):
                sub_state = line.split('=', 1)[1]
            elif line.startswith('MainPID='):
                pid_value = line.split('=', 1)[1]
                main_pid = pid_value if pid_value != "0" else "-"
        
        return active_state, sub_state, main_pid
        
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        # If systemctl is not available or fails, return default values
        return "inactive", "dead", "-"

def main():
    for line in sys.stdin:
        unit_name = line.strip()
        if unit_name:
            active_state, sub_state, main_pid = get_systemd_status(unit_name)
            print(f"{unit_name}: {active_state} sub={sub_state} pid={main_pid}")

if __name__ == "__main__":
    main()