import os
import sys

def get_fd_info(pid):
    try:
        fd_dir = f"/proc/{pid}/fd"
        if not os.path.exists(fd_dir):
            return []
        
        fds = []
        for fd_name in os.listdir(fd_dir):
            try:
                fd_num = int(fd_name)
                fd_path = os.path.join(fd_dir, fd_name)
                
                # Read the symlink target
                try:
                    target = os.readlink(fd_path)
                except (OSError, PermissionError):
                    target = "unknown"
                
                # Determine type and description
                if fd_num == 0:
                    fd_type = "stdin"
                    description = target
                elif fd_num == 1:
                    fd_type = "stdout"
                    description = target
                elif fd_num == 2:
                    fd_type = "stderr"
                    description = target
                elif target.startswith("socket:"):
                    fd_type = "socket"
                    description = target
                elif target.startswith("pipe:"):
                    fd_type = "pipe"
                    description = target
                elif target.startswith("/"):
                    fd_type = "file"
                    description = target
                else:
                    fd_type = "unknown"
                    description = target
                
                fds.append((fd_num, fd_type, description))
            except (ValueError, OSError):
                continue
        
        # Sort by fd number
        fds.sort(key=lambda x: x[0])
        return fds
        
    except (OSError, PermissionError):
        return []

# Read PID from stdin
pid = int(input().strip())

# Get file descriptor info
fd_info = get_fd_info(pid)

# Output results
for fd_num, fd_type, description in fd_info:
    print(f"{fd_num} {fd_type} {description}")