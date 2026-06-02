import socket
import sys
import subprocess
import platform

def get_network_interfaces():
    interfaces = {}
    system = platform.system()
    
    if system == "Linux":
        try:
            # Get interface names and basic info
            with open('/proc/net/dev', 'r') as f:
                lines = f.readlines()[2:]  # Skip header lines
                for line in lines:
                    iface = line.split(':')[0].strip()
                    interfaces[iface] = {'name': iface}
        except:
            pass
        
        # Get IP addresses, netmasks, and status
        try:
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True, timeout=5)
            current_iface = None
            for line in result.stdout.split('\n'):
                line = line.strip()
                if ': ' in line and not line.startswith(' '):
                    parts = line.split(': ')
                    if len(parts) >= 2:
                        iface_info = parts[1].split()
                        current_iface = iface_info[0]
                        if current_iface not in interfaces:
                            interfaces[current_iface] = {'name': current_iface}
                        # Check if interface is UP
                        interfaces[current_iface]['status'] = 'UP' if 'UP' in line else 'DOWN'
                        # Extract MTU
                        if 'mtu' in line.lower():
                            mtu_idx = line.lower().find('mtu')
                            mtu_part = line[mtu_idx:].split()[1]
                            interfaces[current_iface]['mtu'] = mtu_part
                elif current_iface and 'inet ' in line:
                    inet_parts = line.split()
                    for i, part in enumerate(inet_parts):
                        if part == 'inet' and i + 1 < len(inet_parts):
                            interfaces[current_iface]['ip'] = inet_parts[i + 1]
                            break
                elif current_iface and 'link/ether' in line:
                    ether_parts = line.split()
                    for i, part in enumerate(ether_parts):
                        if part == 'link/ether' and i + 1 < len(ether_parts):
                            interfaces[current_iface]['mac'] = ether_parts[i + 1]
                            break
        except:
            pass
            
    # Fallback: ensure loopback exists with basic info
    if 'lo' not in interfaces:
        interfaces['lo'] = {
            'name': 'lo',
            'ip': '127.0.0.1/8',
            'mac': '00:00:00:00:00:00',
            'mtu': '65536',
            'status': 'UP'
        }
    
    # Set defaults for missing values
    for iface in interfaces:
        if 'ip' not in interfaces[iface]:
            interfaces[iface]['ip'] = 'N/A'
        if 'mac' not in interfaces[iface]:
            interfaces[iface]['mac'] = 'N/A'
        if 'mtu' not in interfaces[iface]:
            interfaces[iface]['mtu'] = '1500'
        if 'status' not in interfaces[iface]:
            interfaces[iface]['status'] = 'DOWN'
    
    return interfaces

def main():
    # Check if there's input to filter by interface name
    filter_iface = None
    try:
        input_line = input().strip()
        if input_line:
            filter_iface = input_line
    except EOFError:
        pass
    
    interfaces = get_network_interfaces()
    
    # Sort interfaces for consistent output
    sorted_ifaces = sorted(interfaces.keys())
    
    for iface_name in sorted_ifaces:
        if filter_iface and iface_name != filter_iface:
            continue
            
        iface = interfaces[iface_name]
        ip = iface.get('ip', 'N/A')
        mac = iface.get('mac', 'N/A')
        mtu = iface.get('mtu', '1500')
        status = iface.get('status', 'DOWN')
        
        print(f"{iface_name}: {ip} {mac} mtu={mtu} {status}")

if __name__ == "__main__":
    main()