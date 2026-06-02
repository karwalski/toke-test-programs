import os
import subprocess
import sys

def detect_init_system():
    # Check for systemd
    if os.path.exists('/run/systemd/system') or os.path.exists('/sys/fs/cgroup/systemd'):
        try:
            result = subprocess.run(['systemctl', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines:
                    # First line typically contains "systemd XXX"
                    first_line = lines[0]
                    if 'systemd' in first_line:
                        parts = first_line.split()
                        if len(parts) >= 2:
                            version = parts[1]
                            return 'systemd', version
        except:
            pass
    
    # Check for launchd (macOS)
    if os.path.exists('/System/Library/LaunchDaemons') and os.path.exists('/Library/LaunchDaemons'):
        try:
            result = subprocess.run(['launchctl', 'version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                # Parse launchctl version output
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'launchd' in line.lower():
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if 'launchd' in part.lower() and i + 1 < len(parts):
                                version = parts[i + 1].replace('-', '')
                                return 'launchd', version
            # Fallback - try to get version from system
            result = subprocess.run(['sw_vers', '-productVersion'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                return 'launchd', version
        except:
            pass
    
    # Check for OpenRC
    if os.path.exists('/sbin/openrc') or os.path.exists('/usr/sbin/openrc'):
        try:
            result = subprocess.run(['openrc', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines:
                    # Look for version in output
                    for line in lines:
                        if 'openrc' in line.lower():
                            parts = line.split()
                            for part in parts:
                                if '.' in part and any(c.isdigit() for c in part):
                                    return 'openrc', part
        except:
            pass
    
    # Check for SysV init
    if os.path.exists('/etc/inittab') or os.path.exists('/sbin/init'):
        try:
            # Try to get init version
            result = subprocess.run(['/sbin/init', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                output = result.stdout.strip()
                if 'upstart' in output.lower():
                    lines = output.split('\n')
                    for line in lines:
                        if 'upstart' in line.lower():
                            parts = line.split()
                            for part in parts:
                                if '.' in part and any(c.isdigit() for c in part):
                                    return 'upstart', part
                else:
                    # Generic sysvinit
                    return 'sysvinit', 'unknown'
        except:
            pass
        
        # If we can't get version, but init exists
        if os.path.exists('/sbin/init'):
            return 'sysvinit', 'unknown'
    
    return 'unknown', 'unknown'

def main():
    init_system, version = detect_init_system()
    print(f"Init system: {init_system} version {version}")

if __name__ == "__main__":
    main()