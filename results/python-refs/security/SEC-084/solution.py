import socket
import sys
import json
import struct

def read_ssh_string(data, offset):
    if offset + 4 > len(data):
        return None, offset
    length = struct.unpack('>I', data[offset:offset+4])[0]
    if offset + 4 + length > len(data):
        return None, offset
    return data[offset+4:offset+4+length].decode('utf-8', errors='ignore'), offset + 4 + length

def read_ssh_name_list(data, offset):
    name_list_bytes, new_offset = read_ssh_string(data, offset)
    if name_list_bytes is None:
        return [], new_offset
    if not name_list_bytes:
        return [], new_offset
    return name_list_bytes.split(','), new_offset

def audit_algorithms(kex_algs, ciphers, macs, host_keys):
    issues = []
    
    # Weak KEX algorithms
    weak_kex = ['diffie-hellman-group1-sha1', 'diffie-hellman-group14-sha1', 
                'diffie-hellman-group-exchange-sha1']
    for alg in kex_algs:
        if alg in weak_kex:
            issues.append(f"Weak KEX algorithm: {alg}")
    
    # Weak ciphers
    weak_ciphers = ['3des-cbc', 'aes128-cbc', 'aes192-cbc', 'aes256-cbc', 
                    'arcfour', 'arcfour128', 'arcfour256', 'blowfish-cbc']
    for cipher in ciphers:
        if cipher in weak_ciphers:
            issues.append(f"Weak cipher: {cipher}")
    
    # Weak MACs
    weak_macs = ['hmac-md5', 'hmac-md5-96', 'hmac-sha1-96']
    for mac in macs:
        if mac in weak_macs:
            issues.append(f"Weak MAC: {mac}")
    
    # Weak host key types
    weak_host_keys = ['ssh-dss']
    for key_type in host_keys:
        if key_type in weak_host_keys:
            issues.append(f"Weak host key type: {key_type}")
    
    return issues

def calculate_grade(issues):
    if len(issues) == 0:
        return "A"
    elif len(issues) <= 2:
        return "B"
    elif len(issues) <= 4:
        return "C"
    else:
        return "F"

def connect_ssh(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, port))
        
        # Read banner
        banner = sock.recv(1024).decode('utf-8').strip()
        
        # Send our banner
        our_banner = "SSH-2.0-PythonSSHAudit\r\n"
        sock.send(our_banner.encode())
        
        # Send KEXINIT
        kexinit_payload = b'\x00' * 16  # cookie
        kexinit_payload += struct.pack('>I', 0) + b''  # kex_algorithms (empty)
        kexinit_payload += struct.pack('>I', 0) + b''  # server_host_key_algorithms
        kexinit_payload += struct.pack('>I', 0) + b''  # encryption_algorithms_client_to_server
        kexinit_payload += struct.pack('>I', 0) + b''  # encryption_algorithms_server_to_client
        kexinit_payload += struct.pack('>I', 0) + b''  # mac_algorithms_client_to_server
        kexinit_payload += struct.pack('>I', 0) + b''  # mac_algorithms_server_to_client
        kexinit_payload += struct.pack('>I', 0) + b''  # compression_algorithms_client_to_server
        kexinit_payload += struct.pack('>I', 0) + b''  # compression_algorithms_server_to_client
        kexinit_payload += struct.pack('>I', 0) + b''  # languages_client_to_server
        kexinit_payload += struct.pack('>I', 0) + b''  # languages_server_to_client
        kexinit_payload += b'\x00'  # first_kex_packet_follows
        kexinit_payload += b'\x00' * 4  # reserved
        
        packet = struct.pack('>IB', len(kexinit_payload) + 1, 20) + kexinit_payload
        sock.send(packet)
        
        # Read server's KEXINIT response
        response = sock.recv(4096)
        
        # Parse the response
        if len(response) < 6:
            sock.close()
            return None
        
        packet_length = struct.unpack('>I', response[0:4])[0]
        msg_type = response[5]
        
        if msg_type != 20:  # SSH_MSG_KEXINIT
            sock.close()
            return None
        
        # Skip cookie (16 bytes)
        offset = 22
        
        kex_algorithms, offset = read_ssh_name_list(response, offset)
        host_key_types, offset = read_ssh_name_list(response, offset)
        ciphers_c2s, offset = read_ssh_name_list(response, offset)
        ciphers_s2c, offset = read_ssh_name_list(response, offset)
        macs_c2s, offset = read_ssh_name_list(response, offset)
        macs_s2c, offset = read_ssh_name_list(response, offset)
        
        # Combine client-to-server and server-to-client algorithms
        ciphers = list(set(ciphers_c2s + ciphers_s2c))
        macs = list(set(macs_c2s + macs_s2c))
        
        sock.close()
        
        return {
            'banner': banner,
            'kex_algorithms': kex_algorithms,
            'host_key_types': host_key_types,
            'ciphers': ciphers,
            'macs': macs
        }
        
    except Exception as e:
        return None

def main():
    input_line = sys.stdin.readline().strip()
    host, port = input_line.split(':')
    port = int(port)
    
    result = connect_ssh(host, port)
    
    if result is None:
        output = {
            "host": f"{host}:{port}",
            "banner": "",
            "kexAlgorithms": [],
            "ciphers": [],
            "macs": [],
            "hostKeyTypes": [],
            "issues": ["Connection failed"],
            "grade": "F"
        }
    else:
        issues = audit_algorithms(
            result['kex_algorithms'],
            result['ciphers'],
            result['macs'],
            result['host_key_types']
        )
        
        grade = calculate_grade(issues)
        
        output = {
            "host": f"{host}:{port}",
            "banner": result['banner'],
            "kexAlgorithms": result['kex_algorithms'],
            "ciphers": result['ciphers'],
            "macs": result['macs'],
            "hostKeyTypes": result['host_key_types'],
            "issues": issues,
            "grade": grade
        }
    
    print(output['grade'])

if __name__ == "__main__":
    main()