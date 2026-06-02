import os
import shutil

def get_mounted_partitions():
    partitions = []
    
    # Read /proc/mounts to get mounted filesystems
    try:
        with open('/proc/mounts', 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    device = parts[0]
                    mountpoint = parts[1]
                    fstype = parts[2]
                    
                    # Skip virtual filesystems and common non-disk mounts
                    if (device.startswith('/dev/') and 
                        not fstype in ['proc', 'sysfs', 'devpts', 'tmpfs', 'devtmpfs', 'cgroup', 'pstore', 'debugfs']):
                        
                        try:
                            # Get disk usage statistics
                            statvfs = os.statvfs(mountpoint)
                            total_bytes = statvfs.f_frsize * statvfs.f_blocks
                            free_bytes = statvfs.f_frsize * statvfs.f_bavail
                            used_bytes = total_bytes - free_bytes
                            
                            # Convert to GB
                            total_gb = total_bytes / (1024**3)
                            used_gb = used_bytes / (1024**3)
                            free_gb = free_bytes / (1024**3)
                            
                            # Calculate usage percentage
                            if total_bytes > 0:
                                use_percent = (used_bytes / total_bytes) * 100
                            else:
                                use_percent = 0
                            
                            partitions.append((device, mountpoint, fstype, total_gb, used_gb, free_gb, use_percent))
                        except (OSError, ZeroDivisionError):
                            # Skip if we can't get stats for this mount
                            continue
    except FileNotFoundError:
        # Fallback for non-Linux systems or when /proc/mounts is not available
        # Try to get at least the root partition
        try:
            statvfs = os.statvfs('/')
            total_bytes = statvfs.f_frsize * statvfs.f_blocks
            free_bytes = statvfs.f_frsize * statvfs.f_bavail
            used_bytes = total_bytes - free_bytes
            
            total_gb = total_bytes / (1024**3)
            used_gb = used_bytes / (1024**3)
            free_gb = free_bytes / (1024**3)
            
            if total_bytes > 0:
                use_percent = (used_bytes / total_bytes) * 100
            else:
                use_percent = 0
                
            partitions.append(('/dev/root', '/', 'unknown', total_gb, used_gb, free_gb, use_percent))
        except OSError:
            pass
    
    return partitions

def main():
    partitions = get_mounted_partitions()
    
    for device, mountpoint, fstype, total_gb, used_gb, free_gb, use_percent in partitions:
        print(f"{device} {mountpoint} {fstype} {total_gb:.1f} {used_gb:.1f} {free_gb:.1f} {use_percent:.0f}%")

if __name__ == "__main__":
    main()