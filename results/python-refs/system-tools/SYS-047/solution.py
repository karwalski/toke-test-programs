import subprocess
import sys

def get_logged_in_users():
    try:
        # Use 'who' command to get currently logged-in users
        result = subprocess.run(['who'], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        username = parts[0]
                        tty = parts[1]
                        
                        # Parse login time and from_host
                        if len(parts) >= 5 and '(' in line and ')' in line:
                            # Format: username tty date time (host)
                            date_time_part = ' '.join(parts[2:4])
                            host_start = line.find('(')
                            host_end = line.find(')')
                            from_host = line[host_start+1:host_end] if host_start != -1 and host_end != -1 else ""
                            login_time = date_time_part
                        elif len(parts) >= 4:
                            # Format: username tty date time
                            login_time = ' '.join(parts[2:4])
                            from_host = ""
                        else:
                            login_time = parts[2] if len(parts) > 2 else ""
                            from_host = ""
                        
                        print(f"{username} {tty} {login_time} {from_host}")
        else:
            # Fallback: try to get current user info
            import os
            import getpass
            import time
            
            username = getpass.getuser()
            tty = os.ttyname(sys.stdin.fileno()).split('/')[-1] if sys.stdin.isatty() else "pts/0"
            login_time = time.strftime("%Y-%m-%d %H:%M")
            from_host = ""
            
            print(f"{username} {tty} {login_time} {from_host}")
            
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
        # Fallback for systems without 'who' command or other issues
        import os
        import getpass
        import time
        
        username = getpass.getuser()
        tty = "console"
        login_time = time.strftime("%Y-%m-%d %H:%M")
        from_host = ""
        
        print(f"{username} {tty} {login_time} {from_host}")

if __name__ == "__main__":
    get_logged_in_users()