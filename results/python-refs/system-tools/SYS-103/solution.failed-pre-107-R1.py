import secrets
import string
import sys

def get_charset(charset_type):
    if charset_type == "all":
        return string.ascii_letters + string.digits + string.punctuation
    elif charset_type == "alpha":
        return string.ascii_letters
    elif charset_type == "numeric":
        return string.digits
    elif charset_type == "alnum":
        return string.ascii_letters + string.digits
    elif charset_type == "symbols":
        return string.punctuation
    else:
        raise ValueError(f"Unknown charset type: {charset_type}")

def generate_password(length, charset):
    return ''.join(secrets.choice(charset) for _ in range(length))

# Read input
length = int(input().strip())
charset_type = input().strip()
count = int(input().strip())

# Get the character set
charset = get_charset(charset_type)

# Generate and output passwords
for _ in range(count):
    password = generate_password(length, charset)
    print(password)