import sys
import os

def get_namespace_info(pid):
    """Get namespace information for a given PID"""
    namespaces = ['pid', 'net', 'mnt', 'uts', 'ipc', 'user']
    result = {}
    
    for ns_type in namespaces:
        try:
            ns_path = f"/proc/{pid}/ns/{ns_type}"
            # Read the symbolic link to get the inode
            link_target = os.readlink(ns_path)
            # Extract inode from format like "pid:[4026531836]"
            inode = link_target.split('[')[1].rstrip(']')
            result[ns_type] = inode
        except (OSError, FileNotFoundError, IndexError):
            # If we can't read the namespace, use a placeholder
            result[ns_type] = "unknown"
    
    return result

def main():
    # Read PID from stdin
    pid = input().strip()
    
    # Get namespace information
    ns_info = get_namespace_info(pid)
    
    # Output in the required format
    for ns_type in ['pid', 'net', 'mnt', 'uts', 'ipc', 'user']:
        print(f"{ns_type}: {ns_info[ns_type]}")

if __name__ == "__main__":
    main()