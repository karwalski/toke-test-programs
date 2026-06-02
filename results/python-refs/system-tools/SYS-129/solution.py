import os

def get_mount_info():
    try:
        with open('/proc/mounts', 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 6:
                    device = parts[0]
                    mountpoint = parts[1]
                    fstype = parts[2]
                    options = parts[3]
                    
                    print(f"{device} on {mountpoint} type {fstype} ({options})")
    except FileNotFoundError:
        # Fallback for systems without /proc/mounts
        print("rootfs on / type rootfs (rw)")

get_mount_info()