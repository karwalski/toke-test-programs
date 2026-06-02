import sys
import os
import subprocess

def check_file(path):
    return os.path.exists(path)

def check_process(name):
    try:
        result = subprocess.run(['pgrep', '-f', name], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def check_port(port):
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', int(port)))
        sock.close()
        return result == 0
    except:
        return False

def check_env(name):
    return name in os.environ

def main():
    checks = []
    passed = 0
    total = 0
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split(' ', 1)
        if len(parts) != 2:
            continue
            
        check_type, check_name = parts
        total += 1
        
        if check_type == 'file':
            success = check_file(check_name)
        elif check_type == 'proc':
            success = check_process(check_name)
        elif check_type == 'port':
            success = check_port(check_name)
        elif check_type == 'env':
            success = check_env(check_name)
        else:
            success = False
            
        if success:
            print(f"PASS {check_type} {check_name}")
            passed += 1
        else:
            print(f"FAIL {check_type} {check_name}")
    
    if passed == total:
        print(f"HEALTHY ({passed}/{total} checks passed)")
    else:
        print(f"UNHEALTHY ({passed}/{total} checks passed)")

if __name__ == "__main__":
    main()