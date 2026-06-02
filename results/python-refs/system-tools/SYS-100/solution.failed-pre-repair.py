#!/usr/bin/env python3

import os
import glob

def get_cpu_info():
    # Get list of CPU cores by looking for cpufreq directories
    cpu_dirs = glob.glob('/sys/devices/system/cpu/cpu*/cpufreq')
    cpu_dirs.sort(key=lambda x: int(x.split('cpu')[1].split('/')[0]))
    
    for cpu_dir in cpu_dirs:
        # Extract core number from path
        core_num = int(cpu_dir.split('cpu')[1].split('/')[0])
        
        try:
            # Read current frequency
            with open(os.path.join(cpu_dir, 'scaling_cur_freq'), 'r') as f:
                cur_freq_khz = int(f.read().strip())
                cur_freq_mhz = cur_freq_khz // 1000
            
            # Read min frequency
            with open(os.path.join(cpu_dir, 'scaling_min_freq'), 'r') as f:
                min_freq_khz = int(f.read().strip())
                min_freq_mhz = min_freq_khz // 1000
            
            # Read max frequency
            with open(os.path.join(cpu_dir, 'scaling_max_freq'), 'r') as f:
                max_freq_khz = int(f.read().strip())
                max_freq_mhz = max_freq_khz // 1000
            
            # Read governor
            with open(os.path.join(cpu_dir, 'scaling_governor'), 'r') as f:
                governor = f.read().strip()
            
            print(f"Core {core_num}: cur={cur_freq_mhz}MHz min={min_freq_mhz}MHz max={max_freq_mhz}MHz governor={governor}")
            
        except (FileNotFoundError, PermissionError, ValueError):
            # If we can't read the files, skip this core
            continue

if __name__ == "__main__":
    get_cpu_info()