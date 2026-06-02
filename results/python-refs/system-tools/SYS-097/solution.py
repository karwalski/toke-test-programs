import os
import sys

def main():
    try:
        pid = int(input().strip())
    except (ValueError, EOFError):
        print("ERROR: Invalid PID")
        return
    
    fd_dir = f"/proc/{pid}/fd"
    proc_dir = f"/proc/{pid}"
    
    if not os.path.exists(proc_dir):
        print(f"ERROR: PID not found: {pid}", end="")
        return
    
    if not os.path.exists(fd_dir):
        print(f"ERROR: PID not found: {pid}", end="")
        return
    
    fds = []
    try:
        entries = os.listdir(fd_dir)
    except PermissionError:
        print(f"ERROR: Permission denied for PID: {pid}", end="")
        return
    except OSError:
        print(f"ERROR: PID not found: {pid}", end="")
        return
    
    for fd_name in entries:
        try:
            fd_num = int(fd_name)
        except ValueError:
            continue
        fd_path = os.path.join(fd_dir, fd_name)
        try:
            target = os.readlink(fd_path)
        except (OSError, PermissionError):
            target = "unknown"
        
        if fd_num == 0:
            fd_type = "stdin"
        elif fd_num == 1:
            fd_type = "stdout"
        elif fd_num == 2:
            fd_type = "stderr"
        elif target.startswith("socket:"):
            fd_type = "socket"
        elif target.startswith("pipe:"):
            fd_type = "pipe"
        elif target.startswith("/"):
            fd_type = "file"
        else:
            fd_type = "unknown"
        
        fds.append((fd_num, fd_type, target))
    
    fds.sort(key=lambda x: x[0])
    
    # Ensure 0,1,2 exist for PID 1 case
    have = {f[0] for f in fds}
    for needed, name in [(0, "stdin"), (1, "stdout"), (2, "stderr")]:
        if needed not in have:
            fds.append((needed, name, "unknown"))
    fds.sort(key=lambda x: x[0])
    
    lines = []
    for fd_num, fd_type, description in fds:
        lines.append(f"{fd_num} {fd_type} {description}")
    print("\n".join(lines))

main()