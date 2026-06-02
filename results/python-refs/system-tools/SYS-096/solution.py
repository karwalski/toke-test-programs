import os
import glob

def find_zombie_processes():
    zombies = []
    
    try:
        # Get all process directories in /proc
        proc_dirs = glob.glob('/proc/[0-9]*')
        
        for proc_dir in proc_dirs:
            try:
                # Read the stat file to get process information
                stat_file = os.path.join(proc_dir, 'stat')
                with open(stat_file, 'r') as f:
                    stat_data = f.read().strip()
                
                # Parse the stat data
                # Format: pid (comm) state ppid ...
                parts = stat_data.split()
                if len(parts) >= 4:
                    pid = parts[0]
                    # Command name is in parentheses, might contain spaces
                    comm_start = stat_data.find('(')
                    comm_end = stat_data.rfind(')')
                    if comm_start != -1 and comm_end != -1:
                        comm = stat_data[comm_start+1:comm_end]
                        # Get the part after the command name
                        after_comm = stat_data[comm_end+1:].strip().split()
                        if len(after_comm) >= 2:
                            state = after_comm[0]
                            ppid = after_comm[1]
                            
                            # Check if process is zombie (state 'Z')
                            if state == 'Z':
                                zombies.append((pid, ppid, comm))
            except (IOError, OSError, IndexError, ValueError):
                # Skip processes we can't read (permission denied, etc.)
                continue
                
    except (IOError, OSError):
        # If we can't access /proc, no zombies found
        pass
    
    return zombies

def main():
    zombies = find_zombie_processes()
    
    if zombies:
        for pid, ppid, name in zombies:
            print(f"{pid} {ppid} {name}")
    else:
        print("No zombie processes found")
    
    print(f"Summary: {len(zombies)} zombie processes.")

if __name__ == "__main__":
    main()