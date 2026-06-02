import sys

def audit_password_hashes():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split(',')
        if len(parts) != 3:
            continue
            
        username, hash_value, algorithm = parts
        
        # Check for weak/deprecated algorithms
        if algorithm.lower() == 'md5':
            print(algorithm)
            return
        elif algorithm.lower() == 'sha1':
            print(algorithm)
            return
        elif algorithm.lower() == 'sha256' and not hash_value.startswith('$'):
            print(algorithm)
            return
        elif algorithm.lower() == 'sha512' and not hash_value.startswith('$'):
            print(algorithm)
            return
        elif algorithm.lower() == 'bcrypt':
            # Check bcrypt cost factor
            if hash_value.startswith('$2a$') or hash_value.startswith('$2b$') or hash_value.startswith('$2y$'):
                try:
                    cost_part = hash_value.split('$')[2]
                    cost = int(cost_part)
                    if cost < 10:
                        print(algorithm)
                        return
                except (IndexError, ValueError):
                    pass

if __name__ == "__main__":
    audit_password_hashes()