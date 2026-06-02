import sys
import platform
import subprocess
import os

def get_battery_status():
    system = platform.system()
    
    try:
        if system == "Linux":
            return get_linux_battery_status()
        elif system == "Darwin":  # macOS
            return get_macos_battery_status()
        elif system == "Windows":
            return get_windows_battery_status()
        else:
            return None
    except:
        return None

def get_linux_battery_status():
    # Try to read from /sys/class/power_supply/BAT0/ or similar
    battery_paths = ["/sys/class/power_supply/BAT0", "/sys/class/power_supply/BAT1"]
    
    for bat_path in battery_paths:
        if os.path.exists(bat_path):
            try:
                # Read capacity
                with open(f"{bat_path}/capacity", "r") as f:
                    level = int(f.read().strip())
                
                # Read status
                with open(f"{bat_path}/status", "r") as f:
                    status = f.read().strip().upper()
                
                # Try to get cycle count
                cycle_count = "Unknown"
                if os.path.exists(f"{bat_path}/cycle_count"):
                    with open(f"{bat_path}/cycle_count", "r") as f:
                        cycle_count = f.read().strip()
                
                # Estimate time remaining (simplified)
                time_remaining = "Unknown"
                
                return {
                    "level": level,
                    "status": status,
                    "time_remaining": time_remaining,
                    "cycles": cycle_count
                }
            except:
                continue
    
    return None

def get_macos_battery_status():
    try:
        # Use system_profiler to get battery info
        result = subprocess.run(["system_profiler", "SPPowerDataType"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # Parse the output for battery information
            lines = result.stdout.split('\n')
            level = None
            charging = None
            cycles = None
            
            for line in lines:
                line = line.strip()
                if "State of Charge (%)" in line:
                    level = int(line.split(':')[1].strip())
                elif "Charging" in line and ":" in line:
                    charging_state = line.split(':')[1].strip().lower()
                    if "yes" in charging_state:
                        charging = "CHARGING"
                    else:
                        charging = "DISCHARGING"
                elif "Cycle Count" in line:
                    cycles = line.split(':')[1].strip()
            
            if level is not None:
                return {
                    "level": level,
                    "status": charging or "DISCHARGING",
                    "time_remaining": "Unknown",
                    "cycles": cycles or "Unknown"
                }
    except:
        pass
    
    return None

def get_windows_battery_status():
    try:
        # Use WMIC to get battery info
        result = subprocess.run(["wmic", "path", "Win32_Battery", "get", 
                               "EstimatedChargeRemaining,BatteryStatus"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                data = lines[1].strip().split()
                if len(data) >= 2:
                    battery_status = int(data[0])
                    level = int(data[1])
                    
                    # Battery status codes: 1=Other, 2=Unknown, 3=Full, 4=Low, 5=Critical, 6=Charging, 7=Charging High, 8=Charging Low, 9=Charging Critical, 10=Undefined, 11=Partially Charged
                    if battery_status in [6, 7, 8, 9]:
                        status = "CHARGING"
                    elif battery_status == 3:
                        status = "FULL"
                    else:
                        status = "DISCHARGING"
                    
                    return {
                        "level": level,
                        "status": status,
                        "time_remaining": "Unknown",
                        "cycles": "Unknown"
                    }
    except:
        pass
    
    return None

def main():
    battery_info = get_battery_status()
    
    if battery_info is None:
        print("No battery found")
        return
    
    level = battery_info["level"]
    status = battery_info["status"]
    time_remaining = battery_info["time_remaining"]
    cycles = battery_info["cycles"]
    
    # Format time remaining
    if time_remaining == "Unknown":
        time_str = "time_remaining=Unknown"
    else:
        time_str = f"time_remaining={time_remaining}min"
    
    print(f"Battery: {level}% {status} {time_str} cycles={cycles}")

if __name__ == "__main__":
    main()