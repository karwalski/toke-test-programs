import secrets
import string

def generate_password(length):
    if length < 8:
        length = 8
    
    # Define character classes
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one character from each class
    password = []
    password.append(secrets.choice(uppercase))
    password.append(secrets.choice(lowercase))
    password.append(secrets.choice(digits))
    password.append(secrets.choice(symbols))
    
    # Fill the rest of the password length with random characters from all classes
    all_chars = uppercase + lowercase + digits + symbols
    for _ in range(length - 4):
        password.append(secrets.choice(all_chars))
    
    # Shuffle the password to avoid predictable patterns
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

# Read input
n = int(input())

# Generate and output password
password = generate_password(n)
print(password)