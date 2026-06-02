import sys

def validate_isbn10(isbn):
    # Remove hyphens and spaces
    isbn = isbn.replace('-', '').replace(' ', '')
    
    # Must be exactly 10 characters
    if len(isbn) != 10:
        return False
    
    # Last character can be X or digit, others must be digits
    for i in range(9):
        if not isbn[i].isdigit():
            return False
    
    if not (isbn[9].isdigit() or isbn[9].upper() == 'X'):
        return False
    
    # Calculate checksum
    total = 0
    for i in range(9):
        total += int(isbn[i]) * (10 - i)
    
    if isbn[9].upper() == 'X':
        total += 10
    else:
        total += int(isbn[9])
    
    return total % 11 == 0

def validate_isbn13(isbn):
    # Remove hyphens and spaces
    isbn = isbn.replace('-', '').replace(' ', '')
    
    # Must be exactly 13 digits
    if len(isbn) != 13:
        return False
    
    # All characters must be digits
    if not isbn.isdigit():
        return False
    
    # Calculate checksum
    total = 0
    for i in range(12):
        if i % 2 == 0:
            total += int(isbn[i])
        else:
            total += int(isbn[i]) * 3
    
    check_digit = (10 - (total % 10)) % 10
    return check_digit == int(isbn[12])

def validate_isbn(isbn):
    # Remove hyphens and spaces to determine length
    clean_isbn = isbn.replace('-', '').replace(' ', '')
    
    if len(clean_isbn) == 10:
        return validate_isbn10(isbn)
    elif len(clean_isbn) == 13:
        return validate_isbn13(isbn)
    else:
        return False

# Read from stdin and process each line
for line in sys.stdin:
    isbn = line.strip()
    if isbn:  # Skip empty lines
        if validate_isbn(isbn):
            print(f"{isbn}: VALID")
        else:
            print(f"{isbn}: INVALID")