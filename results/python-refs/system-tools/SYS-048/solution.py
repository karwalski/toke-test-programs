import os
import sys

def parse_ssh_config():
    """Parse ~/.ssh/config file and return a list of host configurations."""
    config_path = os.path.expanduser("~/.ssh/config")
    hosts = []
    
    if not os.path.exists(config_path):
        return hosts
    
    try:
        with open(config_path, 'r') as f:
            lines = f.readlines()
    except:
        return hosts
    
    current_host = None
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        if line.lower().startswith('host '):
            if current_host:
                hosts.append(current_host)
            host_alias = line[5:].strip()
            current_host = {
                'alias': host_alias,
                'hostname': host_alias,  # default to alias
                'user': '',
                'port': '22'  # default SSH port
            }
        elif current_host:
            parts = line.split(None, 1)
            if len(parts) == 2:
                key, value = parts
                key = key.lower()
                if key == 'hostname':
                    current_host['hostname'] = value
                elif key == 'user':
                    current_host['user'] = value
                elif key == 'port':
                    current_host['port'] = value
    
    if current_host:
        hosts.append(current_host)
    
    return hosts

def add_host_to_config(host_data):
    """Add a new host entry to ~/.ssh/config."""
    config_path = os.path.expanduser("~/.ssh/config")
    
    # Ensure .ssh directory exists
    ssh_dir = os.path.dirname(config_path)
    os.makedirs(ssh_dir, exist_ok=True)
    
    # Build host entry
    host_alias = host_data.get('Host', host_data.get('host', ''))
    if not host_alias:
        return False
    
    entry_lines = [f"\nHost {host_alias}\n"]
    
    for key, value in host_data.items():
        if key.lower() != 'host':
            entry_lines.append(f"    {key} {value}\n")
    
    # Append to config file
    try:
        with open(config_path, 'a') as f:
            f.writelines(entry_lines)
        return True
    except:
        return False

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    if not lines:
        return
    
    command = lines[0].strip()
    
    if command == 'list':
        hosts = parse_ssh_config()
        if not hosts:
            print("No hosts configured")
        else:
            for host in hosts:
                print(f"{host['alias']} {host['hostname']} {host['user']} {host['port']}")
    
    elif command == 'add':
        host_data = {}
        for line in lines[1:]:
            if '=' in line:
                key, value = line.split('=', 1)
                host_data[key.strip()] = value.strip()
        
        if host_data:
            host_alias = host_data.get('Host', host_data.get('host', ''))
            if add_host_to_config(host_data):
                print(f"Added host {host_alias} to config.")

if __name__ == "__main__":
    main()