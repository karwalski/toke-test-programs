import os
import sys

def is_pid_alive(pid):
    """Check if a process with given PID is still running."""
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

def acquire_lock(lock_file):
    """Acquire a file-based lock."""
    if os.path.exists(lock_file):
        # Check if existing lock is stale
        try:
            with open(lock_file, 'r') as f:
                old_pid = int(f.read().strip())
            
            if is_pid_alive(old_pid):
                return f"LOCKED_BY {old_pid}"
            else:
                # Remove stale lock
                os.remove(lock_file)
        except (ValueError, IOError):
            # Invalid lock file, remove it
            try:
                os.remove(lock_file)
            except OSError:
                pass
    
    # Acquire the lock
    try:
        with open(lock_file, 'w') as f:
            f.write(str(os.getpid()))
        return "ACQUIRED"
    except IOError:
        return "LOCKED_BY unknown"

def release_lock(lock_file):
    """Release a file-based lock."""
    if not os.path.exists(lock_file):
        return "NOT_LOCKED"
    
    try:
        with open(lock_file, 'r') as f:
            lock_pid = int(f.read().strip())
        
        if lock_pid == os.getpid():
            os.remove(lock_file)
            return "RELEASED"
        else:
            return f"LOCKED_BY {lock_pid}"
    except (ValueError, IOError):
        # Invalid lock file, remove it
        try:
            os.remove(lock_file)
        except OSError:
            pass
        return "NOT_LOCKED"

def check_lock(lock_file):
    """Check the status of a file-based lock."""
    if not os.path.exists(lock_file):
        return "NOT_LOCKED"
    
    try:
        with open(lock_file, 'r') as f:
            lock_pid = int(f.read().strip())
        
        if is_pid_alive(lock_pid):
            return f"LOCKED_BY {lock_pid}"
        else:
            # Remove stale lock
            os.remove(lock_file)
            return "STALE_REMOVED"
    except (ValueError, IOError):
        # Invalid lock file, remove it
        try:
            os.remove(lock_file)
        except OSError:
            pass
        return "NOT_LOCKED"

def main():
    lines = sys.stdin.read().strip().split('\n')
    lock_file = lines[0]
    command = lines[1]
    
    if command == "acquire":
        result = acquire_lock(lock_file)
    elif command == "release":
        result = release_lock(lock_file)
    elif command == "check":
        result = check_lock(lock_file)
    else:
        result = "INVALID_COMMAND"
    
    print(result)

if __name__ == "__main__":
    main()