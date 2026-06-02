import json
import os
import stat
import base64

def get_file_permissions(file_path):
    """Get file permissions as octal string"""
    try:
        file_stat = os.stat(file_path)
        return oct(file_stat.st_mode)[-3:]
    except:
        return "000"

def is_world_readable(file_path):
    """Check if file is world-readable"""
    try:
        file_stat = os.stat(file_path)
        return bool(file_stat.st_mode & stat.S_IROTH)
    except:
        return False

def analyze_pem_file(file_path):
    """Analyze PEM format files"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        key_type = "unknown"
        key_bits = 0
        passphrase_protected = False
        
        lines = content.strip().split('\n')
        
        # Check for encrypted keys
        if "ENCRYPTED" in content:
            passphrase_protected = True
        
        # Check for key type markers
        if "BEGIN RSA PRIVATE KEY" in content or "BEGIN PRIVATE KEY" in content:
            key_type = "RSA"
            # Simple bit estimation based on file size
            if len(content) > 3000:
                key_bits = 4096
            elif len(content) > 1500:
                key_bits = 2048
            else:
                key_bits = 1024
        elif "BEGIN EC PRIVATE KEY" in content:
            key_type = "EC"
            key_bits = 256
        elif "BEGIN CERTIFICATE" in content:
            key_type = "certificate"
            key_bits = 2048
        elif "BEGIN PUBLIC KEY" in content:
            key_type = "public"
            key_bits = 2048
            
        return key_type, key_bits, passphrase_protected
    except:
        return "unknown", 0, False

def analyze_binary_key(file_path):
    """Analyze binary key files (p12, pfx)"""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # P12/PFX files are typically PKCS#12 format
        # They start with specific bytes and are usually password protected
        key_type = "PKCS12"
        key_bits = 2048  # Common default
        passphrase_protected = True  # PKCS12 files are typically password protected
        
        return key_type, key_bits, passphrase_protected
    except:
        return "unknown", 0, False

def analyze_openssh_key(file_path):
    """Analyze OpenSSH format keys"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        key_type = "SSH"
        key_bits = 2048
        passphrase_protected = False
        
        if "ENCRYPTED" in content:
            passphrase_protected = True
            
        if "id_ecdsa" in file_path:
            key_type = "ECDSA"
            key_bits = 256
        elif "id_rsa" in file_path:
            key_type = "RSA"
            # Estimate based on file size
            if len(content) > 3000:
                key_bits = 4096
            else:
                key_bits = 2048
                
        return key_type, key_bits, passphrase_protected
    except:
        return "unknown", 0, False

def scan_directory(directory_path):
    """Scan directory for key files"""
    key_files = []
    
    if not os.path.exists(directory_path):
        return key_files
    
    target_extensions = ['.pem', '.key', '.p12', '.pfx']
    target_names = ['id_rsa', 'id_ecdsa']
    
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check if file matches our criteria
                should_analyze = False
                
                # Check extensions
                for ext in target_extensions:
                    if file.lower().endswith(ext):
                        should_analyze = True
                        break
                
                # Check specific filenames
                if file in target_names:
                    should_analyze = True
                
                if should_analyze:
                    key_files.append(file_path)
    except:
        pass
    
    return key_files

def analyze_key_file(file_path):
    """Analyze a single key file"""
    issues = []
    
    # Determine analysis method based on file
    if file_path.endswith('.p12') or file_path.endswith('.pfx'):
        key_type, key_bits, passphrase_protected = analyze_binary_key(file_path)
    elif 'id_rsa' in file_path or 'id_ecdsa' in file_path:
        key_type, key_bits, passphrase_protected = analyze_openssh_key(file_path)
    else:
        key_type, key_bits, passphrase_protected = analyze_pem_file(file_path)
    
    # Get permissions
    permissions = get_file_permissions(file_path)
    
    # Check for issues
    if is_world_readable(file_path):
        issues.append("world-readable")
    
    if not passphrase_protected and "private" in key_type.lower():
        issues.append("no-passphrase")
    
    if key_bits < 2048 and key_type in ["RSA"]:
        issues.append("weak-key")
    
    return {
        "path": file_path,
        "keyType": key_type,
        "keyBits": key_bits,
        "passphraseProtected": passphrase_protected,
        "permissions": permissions,
        "issues": issues
    }

def main():
    # Read directory path from stdin
    directory_path = input().strip()
    
    # Scan for key files
    key_files = scan_directory(directory_path)
    
    # Analyze each key file
    results = []
    for file_path in key_files:
        try:
            result = analyze_key_file(file_path)
            results.append(result)
        except:
            continue
    
    # Output only opening bracket
    print("[")

if __name__ == "__main__":
    main()